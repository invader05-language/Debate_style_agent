"""
Memory database model for Multi-AI Debate Agent.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, Text, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from backend.database import Base


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

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "topic": self.topic,
            "debate_summary": self.debate_summary,
            "outcome": self.outcome,
            "confidence": self.confidence,
            "tags": self.tags,
            "lessons_learned": self.lessons_learned,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
