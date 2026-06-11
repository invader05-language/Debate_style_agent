"""
API Key database model for Multi-AI Platform v2.0.
Stores encrypted API keys for AI model providers.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from backend.database import Base


class APIKey(Base):
    """Encrypted API key storage."""
    __tablename__ = "api_keys"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    provider = Column(String(50), nullable=False)
    api_key_enc = Column(Text, nullable=False)  # AES-256 encrypted
    key_preview = Column(String(30), nullable=True)  # masked preview like "sk-****3f8a"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": str(self.id),
            "provider": self.provider,
            "key_preview": self.key_preview,
            "is_active": self.is_active,
        }
