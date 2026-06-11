"""
Task Message database model for Multi-AI Platform v2.0.
Stores individual AI outputs within a task (debate turns, think results).
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy import ForeignKey
from backend.database import Base


class TaskMessage(Base):
    """Message within a debate or think task."""
    __tablename__ = "task_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=False)
    model_id = Column(UUID(as_uuid=True), ForeignKey("ai_models.id"), nullable=True)
    role = Column(String(20), nullable=False)  # pro/con/judge/thinker/synthesizer/user/system
    round_number = Column(Integer, nullable=True)
    content = Column(Text, nullable=False)
    structured = Column(JSONB, nullable=True)  # confidence, depth, etc.
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": str(self.id),
            "task_id": str(self.task_id),
            "model_id": str(self.model_id) if self.model_id else None,
            "role": self.role,
            "round_number": self.round_number,
            "content": self.content,
            "structured": self.structured,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
