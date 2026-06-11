"""
端到端集成测试 for Multi-AI Debate Agent.
测试完整流程: API → Engine → Memory → Response.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from httpx import AsyncClient, ASGITransport


def _mock_db_session():
    """Create a mock AsyncSession."""
    from sqlalchemy.ext.asyncio import AsyncSession
    db = AsyncMock(spec=AsyncSession)
    db.execute = AsyncMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    db.close = AsyncMock()
    return db


def _make_debate_model(debate_id="e2e-id", topic="E2E topic",
                       status="pending", action_plan=None, verdict=None):
    """Create a mock DebateModel."""
    from datetime import datetime
    d = MagicMock()
    d.id = debate_id
    d.topic = topic
    d.status = status
    d.action_plan = action_plan
    d.verdict = verdict
    d.created_at = datetime(2026, 6, 4, 12, 0, 0)
    d.completed_at = None
    return d


@pytest.fixture
def mock_db():
    return _mock_db_session()


@pytest.fixture
async def client(mock_db):
    """AsyncClient with mocked DB dependency."""
    from backend.main import app
    from backend.database import get_db

    async def override_get_db():
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


class TestFullDebateFlowE2E:
    """端到端辩论流程测试."""

    @pytest.mark.asyncio
    async def test_create_and_get_debate(self, client, mock_db):
        """测试创建辩论并查询详情."""
        # Step 1: Create debate
        mock_db.refresh = AsyncMock(side_effect=lambda d: setattr(d, 'id', 'e2e-1'))
        mock_db.commit = AsyncMock()

        create_resp = await client.post("/api/debates", json={
            "topic": "Should we use GraphQL or REST?"
        })
        assert create_resp.status_code == 201
        debate_data = create_resp.json()
        assert debate_data["topic"] == "Should we use GraphQL or REST?"
        assert debate_data["status"] == "pending"

    @pytest.mark.asyncio
    async def test_create_list_get_flow(self, client, mock_db):
        """测试创建 → 列表 → 查询完整流程."""
        # Create
        mock_db.commit = AsyncMock()
        await client.post("/api/debates", json={"topic": "Docker vs VM"})

        # List
        mock_count = MagicMock()
        mock_count.scalar.return_value = 1
        mock_debate = _make_debate_model(debate_id="d1", topic="Docker vs VM")
        mock_list_result = MagicMock()
        mock_list_result.scalars.return_value.all.return_value = [mock_debate]
        mock_db.execute = AsyncMock(side_effect=[mock_count, mock_list_result])

        list_resp = await client.get("/api/debates")
        assert list_resp.status_code == 200
        assert list_resp.json()["total"] == 1

        # Get by ID
        mock_get_result = MagicMock()
        mock_get_result.scalar_one_or_none.return_value = mock_debate
        mock_msg_result = MagicMock()
        mock_msg_result.scalars.return_value.all.return_value = []

        with patch("backend.api.debate.cache") as mock_cache:
            mock_cache.get_debate = AsyncMock(return_value=None)
            mock_cache.set_debate = AsyncMock()
            mock_db.execute = AsyncMock(side_effect=[mock_get_result, mock_msg_result])
            get_resp = await client.get("/api/debates/d1")

        assert get_resp.status_code == 200
        assert get_resp.json()["topic"] == "Docker vs VM"

    @pytest.mark.asyncio
    async def test_memory_create_and_search(self, client, mock_db):
        """测试创建记忆并搜索."""
        # Create memory
        mock_db.commit = AsyncMock()

        with patch("backend.api.memory.embedding_service") as mock_emb:
            mock_emb.get_embedding = AsyncMock(return_value=[0.1] * 1024)
            create_resp = await client.post("/api/memories", json={
                "topic": "REST API design",
                "debate_summary": "REST won the debate about API design",
                "outcome": "Implemented REST",
                "confidence": 0.9,
                "tags": ["api", "rest"],
                "lessons_learned": ["REST is simpler for CRUD"]
            })

        assert create_resp.status_code == 201

        # Search memories
        mock_memory = MagicMock()
        mock_memory.id = "mem-1"
        mock_memory.topic = "REST API design"
        mock_memory.debate_summary = "REST won the debate about API design"
        mock_memory.outcome = "Implemented REST"
        mock_memory.confidence = 0.9
        mock_memory.tags = ["api", "rest"]
        mock_memory.lessons_learned = ["REST is simpler for CRUD"]
        mock_memory.created_at = MagicMock()
        mock_memory.created_at.isoformat.return_value = "2026-06-04T12:00:00"

        mock_search_result = MagicMock()
        mock_search_result.scalars.return_value.all.return_value = [mock_memory]
        mock_db.execute = AsyncMock(return_value=mock_search_result)

        with patch("backend.api.memory.cache") as mock_cache:
            mock_cache.get_memory_search = AsyncMock(return_value=None)
            mock_cache.set_memory_search = AsyncMock()
            search_resp = await client.get("/api/memories/search?q=REST")

        assert search_resp.status_code == 200
        results = search_resp.json()
        assert len(results) > 0


class TestHealthEndpointsE2E:
    """端到端健康检查测试."""

    @pytest.mark.asyncio
    async def test_root_and_health(self, client):
        """测试根路径和健康检查."""
        root_resp = await client.get("/")
        assert root_resp.status_code == 200
        assert "message" in root_resp.json()

        health_resp = await client.get("/health")
        assert health_resp.status_code == 200
        assert health_resp.json()["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_404_for_unknown_route(self, client):
        """测试未知路由返回 404."""
        resp = await client.get("/api/unknown/endpoint")
        assert resp.status_code == 404


class TestAuthFlowE2E:
    """端到端认证流程测试."""

    @pytest.mark.asyncio
    async def test_register_then_login(self, client, mock_db):
        """测试注册后登录流程."""
        # Register
        mock_no_user = MagicMock()
        mock_no_user.scalar_one_or_none.return_value = None
        mock_db.execute = AsyncMock(return_value=mock_no_user)
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()

        reg_resp = await client.post("/api/auth/register", json={
            "username": "e2euser",
            "email": "e2e@example.com",
            "password": "testpassword123"
        })
        assert reg_resp.status_code == 201

        # Login
        from passlib.hash import bcrypt
        mock_user = MagicMock()
        mock_user.id = "user-e2e"
        mock_user.username = "e2euser"
        mock_user.email = "e2e@example.com"
        mock_user.hashed_password = bcrypt.hash("testpassword123")
        mock_user.is_active = True

        mock_login_result = MagicMock()
        mock_login_result.scalar_one_or_none.return_value = mock_user
        mock_db.execute = AsyncMock(return_value=mock_login_result)

        login_resp = await client.post("/api/auth/login", json={
            "username": "e2euser",
            "password": "testpassword123"
        })
        assert login_resp.status_code == 200
        data = login_resp.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
