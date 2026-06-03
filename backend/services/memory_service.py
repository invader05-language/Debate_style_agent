"""
Memory service for Multi-AI Debate Agent.
Business logic for memory operations.
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.models.memory import MemoryModel
from backend.cache import cache


class MemoryService:
    """Service for memory operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_memory(self, topic: str, debate_summary: str,
                           outcome: str = None, confidence: float = 0.5,
                           tags: List[str] = None,
                           lessons_learned: List[str] = None) -> MemoryModel:
        """Create a new memory."""
        memory = MemoryModel(
            topic=topic,
            debate_summary=debate_summary,
            outcome=outcome,
            confidence=confidence,
            tags=tags or [],
            lessons_learned=lessons_learned or []
        )
        self.db.add(memory)
        await self.db.commit()
        await self.db.refresh(memory)
        return memory

    async def search_memories(self, query: str, limit: int = 10) -> List[MemoryModel]:
        """Search memories by text."""
        # Try cache first
        cached = await cache.get_memory_search(query)
        if cached:
            return cached

        # Search in database
        stmt = select(MemoryModel).where(
            MemoryModel.topic.ilike(f"%{query}%") |
            MemoryModel.debate_summary.ilike(f"%{query}%")
        ).limit(limit)
        result = await self.db.execute(stmt)
        memories = result.scalars().all()

        # Cache the result
        if memories:
            await cache.set_memory_search(query, [m.to_dict() for m in memories])

        return memories

    async def get_relevant_memories(self, topic: str, limit: int = 3) -> List[MemoryModel]:
        """Get relevant memories for a topic."""
        # First try exact topic match
        stmt = select(MemoryModel).where(
            MemoryModel.topic.ilike(f"%{topic}%")
        ).limit(limit)
        result = await self.db.execute(stmt)
        memories = result.scalars().all()

        if memories:
            return memories

        # Then try keyword search
        keywords = topic.split()[:3]
        all_memories = []

        for keyword in keywords:
            stmt = select(MemoryModel).where(
                MemoryModel.topic.ilike(f"%{keyword}%") |
                MemoryModel.debate_summary.ilike(f"%{keyword}%")
            ).limit(2)
            result = await self.db.execute(stmt)
            all_memories.extend(result.scalars().all())

        # Deduplicate
        seen_ids = set()
        unique_memories = []
        for mem in all_memories:
            if mem.id not in seen_ids:
                seen_ids.add(mem.id)
                unique_memories.append(mem)
                if len(unique_memories) >= limit:
                    break

        return unique_memories
