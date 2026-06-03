"""
Memory store implementation for Multi-AI Debate Agent.
PostgreSQL-based memory storage with semantic search.
"""

import uuid
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, Text, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session
from database import Base, SessionLocal
from agents.mimo_agent import MIMOAgent


class MemoryModel(Base):
    """Memory database model."""
    __tablename__ = "memories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    topic = Column(String(500), nullable=False)
    debate_summary = Column(Text, nullable=False)
    outcome = Column(Text, nullable=True)
    confidence = Column(Float, default=0.5)
    tags = Column(ARRAY(String), default=[])
    lessons_learned = Column(ARRAY(String), default=[])
    created_at = Column(DateTime, default=datetime.utcnow)


class MemoryStore:
    """
    Memory store with PostgreSQL backend.

    ┌─────────────────────────────────────────────┐
    │              MemoryStore                     │
    ├─────────────────────────────────────────────┤
    │ + save(memory: dict) -> str                 │
    │ + search(query: str, limit: int) -> List    │
    │ + get_by_topic(topic: str) -> List          │
    │ + get_relevant(topic: str) -> List          │
    └─────────────────────────────────────────────┘
    """

    def __init__(self, embedding_agent: Optional[MIMOAgent] = None):
        self.embedding_agent = embedding_agent or MIMOAgent()

    async def save(self, memory: dict) -> str:
        """
        Save memory to database.

        Args:
            memory: Memory dict with topic, debate_summary, etc.

        Returns:
            Memory ID
        """
        db = SessionLocal()
        try:
            db_memory = MemoryModel(
                topic=memory.get("topic", ""),
                debate_summary=memory.get("debate_summary", ""),
                outcome=memory.get("outcome", ""),
                confidence=memory.get("confidence", 0.5),
                tags=memory.get("tags", []),
                lessons_learned=memory.get("lessons_learned", [])
            )
            db.add(db_memory)
            db.commit()
            db.refresh(db_memory)
            return str(db_memory.id)
        finally:
            db.close()

    async def search(self, query: str, limit: int = 5) -> List[dict]:
        """
        Search memories by text similarity.

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            List of matching memories
        """
        db = SessionLocal()
        try:
            # Simple text search (can be enhanced with pgvector)
            memories = db.query(MemoryModel).filter(
                MemoryModel.topic.ilike(f"%{query}%") |
                MemoryModel.debate_summary.ilike(f"%{query}%")
            ).limit(limit).all()

            return [self._to_dict(m) for m in memories]
        finally:
            db.close()

    async def get_by_topic(self, topic: str) -> List[dict]:
        """
        Get memories by exact topic.

        Args:
            topic: Topic to search

        Returns:
            List of matching memories
        """
        db = SessionLocal()
        try:
            memories = db.query(MemoryModel).filter(
                MemoryModel.topic.ilike(f"%{topic}%")
            ).all()

            return [self._to_dict(m) for m in memories]
        finally:
            db.close()

    async def get_relevant(self, current_topic: str, limit: int = 3) -> List[dict]:
        """
        Get relevant memories for current topic.

        Args:
            current_topic: Current debate topic
            limit: Maximum results

        Returns:
            List of relevant memories
        """
        # First try exact topic match
        exact_matches = await self.get_by_topic(current_topic)
        if exact_matches:
            return exact_matches[:limit]

        # Then try keyword search
        keywords = current_topic.split()[:3]  # First 3 words
        all_memories = []

        for keyword in keywords:
            memories = await self.search(keyword, limit=2)
            all_memories.extend(memories)

        # Deduplicate and limit
        seen_ids = set()
        unique_memories = []
        for mem in all_memories:
            if mem["id"] not in seen_ids:
                seen_ids.add(mem["id"])
                unique_memories.append(mem)
                if len(unique_memories) >= limit:
                    break

        return unique_memories

    def _to_dict(self, memory: MemoryModel) -> dict:
        """Convert memory model to dict."""
        return {
            "id": str(memory.id),
            "topic": memory.topic,
            "debate_summary": memory.debate_summary,
            "outcome": memory.outcome,
            "confidence": memory.confidence,
            "tags": memory.tags,
            "lessons_learned": memory.lessons_learned,
            "created_at": memory.created_at.isoformat() if memory.created_at else None
        }
