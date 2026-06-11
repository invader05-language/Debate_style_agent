"""
Debate service for Multi-AI Debate Agent.
Business logic for debate operations.
"""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.models.debate import DebateModel
from backend.models.message import MessageModel
from backend.cache import cache
from debate.engine import DebateEngine
from debate.protocol import DebateConfig
from memory.store import MemoryStore


class DebateService:
    """Service for debate operations."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.memory_store = MemoryStore()
        self.engine = DebateEngine(memory_store=self.memory_store)

    async def create_debate(self, topic: str) -> DebateModel:
        """Create a new debate."""
        debate = DebateModel(topic=topic, status="pending")
        self.db.add(debate)
        await self.db.commit()
        await self.db.refresh(debate)
        return debate

    async def get_debate(self, debate_id: str) -> Optional[DebateModel]:
        """Get debate by ID."""
        # Try cache first
        cached = await cache.get_debate(debate_id)
        if cached:
            return cached

        # Get from database
        query = select(DebateModel).where(DebateModel.id == debate_id)
        result = await self.db.execute(query)
        debate = result.scalar_one_or_none()

        if debate:
            # Cache the result
            await cache.set_debate(debate_id, debate.to_dict())

        return debate

    async def start_debate(self, debate_id: str) -> Optional[DebateModel]:
        """Start a debate."""
        debate = await self.get_debate(debate_id)
        if not debate:
            return None

        if debate.status != "pending":
            return None

        debate.status = "running"
        await self.db.commit()

        return debate

    async def run_debate(self, debate: DebateModel, config: DebateConfig):
        """Run the debate engine."""
        try:
            # Run debate
            result = await self.engine.start_debate(config)

            # Update debate
            debate.status = "completed"
            debate.completed_at = result.completed_at
            debate.verdict = result.verdict.dict() if result.verdict else None
            debate.action_plan = result.verdict.action_plan if result.verdict else None

            # Save messages
            for round in result.rounds:
                for msg in [round.pro_message, round.con_message, round.judge_message]:
                    if msg:
                        db_msg = MessageModel(
                            debate_id=debate.id,
                            round_number=msg.round_number,
                            role=msg.role,
                            content=msg.content,
                            model_used=msg.model_used,
                            confidence=msg.confidence
                        )
                        self.db.add(db_msg)

            await self.db.commit()

            # Clear cache
            await cache.delete(f"debate:{debate.id}")

            return result

        except Exception as e:
            debate.status = "failed"
            await self.db.commit()
            raise e
