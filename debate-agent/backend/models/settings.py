"""
User Settings database model for Multi-AI Platform v2.0.
Stores user preferences (language, theme, notifications).
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from backend.database import Base


class UserSettings(Base):
    """User preferences."""
    __tablename__ = "user_settings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, default=uuid.UUID("00000000-0000-0000-0000-000000000001"))
    language = Column(String(10), default="zh")
    theme_mode = Column(String(10), default="light")
    notifications = Column(Boolean, default=True)
    weekly_digest = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": str(self.id),
            "language": self.language,
            "theme_mode": self.theme_mode,
            "notifications": self.notifications,
            "weekly_digest": self.weekly_digest,
        }
