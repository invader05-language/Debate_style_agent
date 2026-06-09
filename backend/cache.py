"""
Redis cache implementation for Multi-AI Debate Agent.
"""

import json
import logging
from typing import Optional, Any
from backend.config import config

logger = logging.getLogger(__name__)


class RedisCache:
    """Redis cache for debate results and memory queries."""

    def __init__(self):
        self._redis = None

    def _get_redis(self):
        if self._redis is None:
            try:
                import redis.asyncio as redis
                self._redis = redis.from_url(config.REDIS_URL, decode_responses=True)
            except Exception as e:
                logger.warning(f"Redis not available: {e}")
                return None
        return self._redis

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        r = self._get_redis()
        if r is None:
            return None
        try:
            value = await r.get(key)
            if value:
                return json.loads(value)
        except Exception:
            pass
        return None

    async def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        """Set value in cache with TTL (seconds)."""
        r = self._get_redis()
        if r is None:
            return
        try:
            await r.set(key, json.dumps(value), ex=ttl)
        except Exception:
            pass

    async def delete(self, key: str) -> None:
        """Delete value from cache."""
        r = self._get_redis()
        if r is None:
            return
        try:
            await r.delete(key)
        except Exception:
            pass

    async def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        r = self._get_redis()
        if r is None:
            return False
        try:
            return await r.exists(key) > 0
        except Exception:
            return False

    async def get_debate(self, debate_id: str) -> Optional[dict]:
        """Get debate from cache."""
        return await self.get(f"debate:{debate_id}")

    async def set_debate(self, debate_id: str, debate: dict, ttl: int = 1800) -> None:
        """Set debate in cache (30 min TTL)."""
        await self.set(f"debate:{debate_id}", debate, ttl)

    async def get_memory_search(self, query: str) -> Optional[list]:
        """Get memory search results from cache."""
        return await self.get(f"memory_search:{query}")

    async def set_memory_search(self, query: str, results: list, ttl: int = 300) -> None:
        """Set memory search results in cache (5 min TTL)."""
        await self.set(f"memory_search:{query}", results, ttl)

    async def close(self):
        """Close Redis connection."""
        if self._redis:
            await self._redis.close()
            self._redis = None

    async def health_check(self) -> dict:
        """
        Check Redis connectivity and return status.

        Returns:
            dict with status, latency_ms, and error (if any)
        """
        r = self._get_redis()
        if r is None:
            return {"status": "unavailable", "latency_ms": None, "error": "Redis not configured"}
        try:
            import time
            start = time.time()
            await r.ping()
            latency_ms = round((time.time() - start) * 1000, 2)
            return {"status": "connected", "latency_ms": latency_ms, "error": None}
        except Exception as e:
            return {"status": "error", "latency_ms": None, "error": str(e)}

    async def flush_pattern(self, pattern: str) -> int:
        """
        Delete all keys matching a pattern.

        Args:
            pattern: Redis key pattern (e.g., "memory_search:*")

        Returns:
            Number of keys deleted
        """
        r = self._get_redis()
        if r is None:
            return 0
        try:
            keys = []
            async for key in r.scan_iter(match=pattern):
                keys.append(key)
            if keys:
                return await r.delete(*keys)
            return 0
        except Exception as e:
            logger.warning(f"Failed to flush pattern {pattern}: {e}")
            return 0


# Global cache instance (lazy — no connection until first use)
cache = RedisCache()
