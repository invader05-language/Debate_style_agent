"""
Redis cache implementation for Multi-AI Debate Agent.
"""

import json
from typing import Optional, Any
import redis.asyncio as redis
from backend.config import config


class RedisCache:
    """Redis cache for debate results and memory queries."""

    def __init__(self):
        self.redis = redis.from_url(config.REDIS_URL, decode_responses=True)

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        value = await self.redis.get(key)
        if value:
            return json.loads(value)
        return None

    async def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        """Set value in cache with TTL (seconds)."""
        await self.redis.set(key, json.dumps(value), ex=ttl)

    async def delete(self, key: str) -> None:
        """Delete value from cache."""
        await self.redis.delete(key)

    async def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        return await self.redis.exists(key) > 0

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
        await self.redis.close()


# Global cache instance
cache = RedisCache()
