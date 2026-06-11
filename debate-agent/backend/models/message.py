"""
Message database model for Multi-AI Debate Agent.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey
from backend.database import Base


class MessageModel(Base):
    """Message database model."""
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    debate_id = Column(UUID(as_uuid=True), ForeignKey("debates.id"), nullable=False)
    round_number = Column(Integer, nullable=False)
    role = Column(String(20), nullable=False)  # pro/con/judge
    content = Column(Text, nullable=False)
    model_used = Column(String(50), nullable=False)
    confidence = Column(Float, default=0.8)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "debate_id": str(self.debate_id),
            "round_number": self.round_number,
            "role": self.role,
            "content": self.content,
            "model_used": self.model_used,
            "confidence": self.confidence,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
