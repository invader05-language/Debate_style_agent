"""
Task database model for Multi-AI Platform v2.0.
Unified table for both debate and think tasks.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from backend.database import Base


class Task(Base):
    """Unified task table for debates and think sessions."""
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String(20), nullable=False)  # debate/think
    topic = Column(Text, nullable=False)
    status = Column(String(20), default="pending")  # pending/running/completed/failed
    config = Column(JSONB, nullable=True)  # task configuration (rounds, models, etc.)
    result = Column(JSONB, nullable=True)  # final result (verdict, synthesis)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": str(self.id),
            "type": self.type,
            "topic": self.topic,
            "status": self.status,
            "config": self.config,
            "result": self.result,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }
