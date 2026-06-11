"""
性能压测脚本 for Multi-AI Debate Agent.
使用 pytest-benchmark 或手动计时测试关键 API 端点性能。
"""

import pytest
import asyncio
import time
from unittest.mock import AsyncMock, MagicMock, patch
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession


def _mock_db_session():
    db = AsyncMock(spec=AsyncSession)
    db.execute = AsyncMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    db.close = AsyncMock()
    return db


def _make_debate_model(debate_id="perf-id", topic="Perf test", status="pending"):
    from datetime import datetime
    d = MagicMock()
    d.id = debate_id
    d.topic = topic
    d.status = status
    d.action_plan = None
    d.verdict = None
    d.created_at = datetime(2026, 6, 4, 12, 0, 0)
    d.completed_at = None
    return d


@pytest.fixture
def mock_db():
    return _mock_db_session()


@pytest.fixture
async def client(mock_db):
    from backend.main import app
    from backend.database import get_db

    async def override_get_db():
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


class TestAPIPerformance:
    """API 性能基准测试."""

    @pytest.mark.asyncio
    async def test_root_latency(self, client):
        """测试根端点延迟 < 50ms."""
        start = time.perf_counter()
        for _ in range(10):
            await client.get("/")
        elapsed = (time.perf_counter() - start) / 10
        assert elapsed < 0.05, f"Root endpoint avg latency {elapsed:.4f}s > 50ms"

    @pytest.mark.asyncio
    async def test_health_latency(self, client):
        """测试健康检查延迟 < 50ms."""
        start = time.perf_counter()
        for _ in range(10):
            await client.get("/health")
        elapsed = (time.perf_counter() - start) / 10
        assert elapsed < 0.05, f"Health endpoint avg latency {elapsed:.4f}s > 50ms"

    @pytest.mark.asyncio
    async def test_create_debate_latency(self, client, mock_db):
        """测试创建辩论延迟 < 100ms."""
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock(side_effect=lambda d: setattr(d, 'id', 'perf-1'))

        start = time.perf_counter()
        for i in range(5):
            await client.post("/api/debates", json={"topic": f"Perf test {i}"})
        elapsed = (time.perf_counter() - start) / 5
        assert elapsed < 0.1, f"Create debate avg latency {elapsed:.4f}s > 100ms"

    @pytest.mark.asyncio
    async def test_list_debates_latency(self, client, mock_db):
        """测试列表查询延迟 < 100ms."""
        mock_count = MagicMock()
        mock_count.scalar.return_value = 0
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db.execute = AsyncMock(side_effect=[mock_count, mock_result])

        start = time.perf_counter()
        for _ in range(10):
            await client.get("/api/debates")
        elapsed = (time.perf_counter() - start) / 10
        assert elapsed < 0.1, f"List debates avg latency {elapsed:.4f}s > 100ms"

    @pytest.mark.asyncio
    async def test_concurrent_requests(self, client, mock_db):
        """测试 50 并发请求不报错."""
        mock_count = MagicMock()
        mock_count.scalar.return_value = 0
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = []
        mock_db.execute = AsyncMock(side_effect=[mock_count, mock_result])

        async def single_request():
            resp = await client.get("/api/debates")
            return resp.status_code

        tasks = [single_request() for _ in range(50)]
        results = await asyncio.gather(*tasks)

        success_count = sum(1 for s in results if s == 200)
        assert success_count >= 45, f"Only {success_count}/50 requests succeeded"

    @pytest.mark.asyncio
    async def test_concurrent_create_debate(self, client, mock_db):
        """测试 20 并发创建辩论."""
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock(side_effect=lambda d: setattr(d, 'id', 'c-1'))

        async def create_one(i):
            resp = await client.post("/api/debates", json={"topic": f"Concurrent {i}"})
            return resp.status_code

        tasks = [create_one(i) for i in range(20)]
        results = await asyncio.gather(*tasks)

        success_count = sum(1 for s in results if s == 201)
        assert success_count >= 18, f"Only {success_count}/20 creates succeeded"


class TestRateLimiterPerformance:
    """限流器性能测试."""

    def test_rate_limiter_check_speed(self):
        """测试限流器检查速度 < 1ms/次."""
        from backend.middleware import RateLimiter
        limiter = RateLimiter(requests_per_minute=1000)

        start = time.perf_counter()
        for i in range(1000):
            limiter.check_sync = lambda ip: True
            # Use the actual async check in sync wrapper
            loop = asyncio.new_event_loop()
            loop.run_until_complete(limiter.check("127.0.0.1", "/test"))
            loop.close()
        elapsed = (time.perf_counter() - start) / 1000
        assert elapsed < 0.001, f"Rate limiter check {elapsed:.6f}s > 1ms"

    def test_rate_limiter_cleanup_efficiency(self):
        """测试过期条目清理效率."""
        from backend.middleware import RateLimiter
        import time as time_mod
        limiter = RateLimiter(requests_per_minute=60, cleanup_interval=0)

        # Add 1000 expired entries
        old_time = time_mod.time() - 120
        for i in range(1000):
            limiter.requests[f"ip-{i}"].append(old_time)

        start = time.perf_counter()
        limiter._cleanup_expired()
        elapsed = time.perf_counter() - start

        assert elapsed < 0.1, f"Cleanup took {elapsed:.4f}s for 1000 entries"
        assert len(limiter.requests) == 0


class TestCachePerformance:
    """缓存性能测试."""

    @pytest.mark.asyncio
    async def test_cache_miss_latency(self):
        """测试缓存未命中延迟."""
        from backend.cache import RedisCache
        cache = RedisCache()
        cache._redis = None  # Force miss

        start = time.perf_counter()
        for _ in range(100):
            await cache.get("nonexistent")
        elapsed = (time.perf_counter() - start) / 100
        assert elapsed < 0.001, f"Cache miss {elapsed:.6f}s > 1ms"
