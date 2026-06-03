"""
Debate database model for Multi-AI Debate Agent.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSONB
from sqlalchemy.dialects.postgresql import UUID
from backend.database import Base


class DebateModel(Base):
    """Debate database model."""
    __tablename__ = "debates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    topic = Column(String(500), nullable=False)
    status = Column(String(20), default="pending")  # pending/running/completed/executed/failed
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    verdict = Column(JSONB, nullable=True)
    action_plan = Column(JSONB, nullable=True)

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "topic": self.topic,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "verdict": self.verdict,
            "action_plan": self.action_plan
        }
