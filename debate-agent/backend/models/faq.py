"""
FAQ database model for Multi-AI Platform v2.0.
Stores help center frequently asked questions.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from backend.database import Base


class FAQ(Base):
    """Help center FAQ entry."""
    __tablename__ = "faqs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    category = Column(String(50), default="general")  # debate/think/model/general
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": str(self.id),
            "question": self.question,
            "answer": self.answer,
            "category": self.category,
            "sort_order": self.sort_order,
        }
