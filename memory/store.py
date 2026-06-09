"""
Memory store implementation for Multi-AI Debate Agent.
PostgreSQL-based memory storage with pgvector semantic search.
Uses async sessions from backend.database.
"""

import logging
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import text, select
from backend.database import AsyncSessionLocal
from backend.models.memory import MemoryModel

if TYPE_CHECKING:
    from agents.mimo_agent import MIMOAgent

logger = logging.getLogger(__name__)


class MemoryStore:
    """
    Memory store with PostgreSQL backend and pgvector semantic search.

    Uses cosine similarity on embedding vectors for semantic search,
    with ILIKE text search as fallback when embeddings are unavailable.
    """

    def __init__(self, embedding_agent: Optional['MIMOAgent'] = None):
        if embedding_agent is None:
            # Lazy import to avoid circular dependency
            from agents.mimo_agent import MIMOAgent
            embedding_agent = MIMOAgent()
        self.embedding_agent = embedding_agent

    async def save(self, memory: dict) -> str:
        """Save memory to database with optional embedding generation."""
        async with AsyncSessionLocal() as db:
            try:
                # Generate embedding for semantic search
                embedding = None
                try:
                    embedding_text = f"{memory.get('topic', '')} {memory.get('debate_summary', '')}"
                    embedding = await self.embedding_agent.get_embedding(embedding_text)
                except Exception as e:
                    logger.warning(f"Failed to generate embedding: {e}")

                db_memory = MemoryModel(
                    topic=memory.get("topic", ""),
                    debate_summary=memory.get("debate_summary", ""),
                    outcome=memory.get("outcome", ""),
                    confidence=memory.get("confidence", 0.5),
                    tags=memory.get("tags", []),
                    lessons_learned=memory.get("lessons_learned", [])
                )

                if embedding:
                    db_memory.embedding = embedding

                db.add(db_memory)
                await db.commit()
                await db.refresh(db_memory)
                return str(db_memory.id)
            except Exception:
                await db.rollback()
                raise

    async def search(self, query: str, limit: int = 5) -> List[dict]:
        """Search memories by semantic similarity using pgvector."""
        async with AsyncSessionLocal() as db:
            try:
                # Try semantic search first
                embedding = None
                try:
                    embedding = await self.embedding_agent.get_embedding(query)
                except Exception as e:
                    logger.warning(f"Embedding generation failed, falling back to text search: {e}")

                if embedding:
                    stmt = text("""
                        SELECT *, 1 - (embedding <=> :query_embedding::vector) as similarity
                        FROM memories
                        WHERE embedding IS NOT NULL
                        ORDER BY embedding <=> :query_embedding::vector
                        LIMIT :limit
                    """)
                    result = await db.execute(stmt, {
                        "query_embedding": str(embedding),
                        "limit": limit
                    })
                    rows = result.fetchall()

                    if rows:
                        return [self._row_to_dict(row) for row in rows]

                # Fallback to ILIKE text search
                stmt = select(MemoryModel).where(
                    MemoryModel.topic.ilike(f"%{query}%") |
                    MemoryModel.debate_summary.ilike(f"%{query}%")
                ).limit(limit)
                result = await db.execute(stmt)
                memories = result.scalars().all()

                return [self._to_dict(m) for m in memories]
            except Exception:
                await db.rollback()
                raise

    async def get_by_topic(self, topic: str) -> List[dict]:
        """Get memories by exact topic."""
        async with AsyncSessionLocal() as db:
            stmt = select(MemoryModel).where(
                MemoryModel.topic.ilike(f"%{topic}%")
            )
            result = await db.execute(stmt)
            memories = result.scalars().all()
            return [self._to_dict(m) for m in memories]

    async def get_relevant(self, current_topic: str, limit: int = 3) -> List[dict]:
        """Get relevant memories for current topic using semantic search."""
        # Try semantic search first
        embedding = None
        try:
            embedding = await self.embedding_agent.get_embedding(current_topic)
        except Exception as e:
            logger.warning(f"Embedding failed for get_relevant: {e}")

        if embedding:
            async with AsyncSessionLocal() as db:
                stmt = text("""
                    SELECT *, 1 - (embedding <=> :query_embedding::vector) as similarity
                    FROM memories
                    WHERE embedding IS NOT NULL
                    ORDER BY embedding <=> :query_embedding::vector
                    LIMIT :limit
                """)
                result = await db.execute(stmt, {
                    "query_embedding": str(embedding),
                    "limit": limit
                })
                rows = result.fetchall()

                if rows:
                    return [self._row_to_dict(row) for row in rows]

        # Fallback to topic match
        exact_matches = await self.get_by_topic(current_topic)
        if exact_matches:
            return exact_matches[:limit]

        # Then try keyword search
        keywords = current_topic.split()[:3]
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

    def _row_to_dict(self, row) -> dict:
        """Convert database row to dict (includes similarity score)."""
        return {
            "id": str(row.id),
            "topic": row.topic,
            "debate_summary": row.debate_summary,
            "outcome": row.outcome,
            "confidence": row.confidence,
            "tags": row.tags,
            "lessons_learned": row.lessons_learned,
            "created_at": row.created_at.isoformat() if row.created_at else None,
            "similarity": float(row.similarity) if hasattr(row, 'similarity') else None
        }
