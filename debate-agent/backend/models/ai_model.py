"""
AI Model database model for Multi-AI Platform v2.0.
Stores registered AI model configurations.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from backend.database import Base


class AIModel(Base):
    """AI Model registry."""
    __tablename__ = "ai_models"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    provider = Column(String(50), nullable=False)  # mimo/deepseek/openai/anthropic/google/custom
    model_id = Column(String(100), nullable=False)
    api_url = Column(String(500), nullable=False)
    api_key = Column(String(500), nullable=False)  # encrypted
    api_format = Column(String(20), default="openai")  # openai/anthropic/gemini
    max_tokens = Column(Integer, default=4096)
    temperature = Column(Float, default=0.7)
    is_preset = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    icon = Column(String(50), nullable=True)
    color = Column(String(20), nullable=True)
    last_tested_at = Column(DateTime, nullable=True)
    last_test_status = Column(String(20), nullable=True)  # success/failed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "provider": self.provider,
            "model_id": self.model_id,
            "api_url": self.api_url,
            "api_format": self.api_format,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "is_preset": self.is_preset,
            "is_active": self.is_active,
            "icon": self.icon,
            "color": self.color,
            "last_tested_at": self.last_tested_at.isoformat() if self.last_tested_at else None,
            "last_test_status": self.last_test_status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
