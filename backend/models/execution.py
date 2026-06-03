"""
Execution database model for Multi-AI Debate Agent.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey
from backend.database import Base


class ExecutionModel(Base):
    """Execution database model."""
    __tablename__ = "executions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    debate_id = Column(UUID(as_uuid=True), ForeignKey("debates.id"), nullable=False)
    status = Column(String(20), default="pending")  # pending/running/success/failed
    code_generated = Column(Text, nullable=True)
    execution_result = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    def to_dict(self):
        """Convert to dictionary."""
        return {
            "id": str(self.id),
            "debate_id": str(self.debate_id),
            "status": self.status,
            "code_generated": self.code_generated,
            "execution_result": self.execution_result,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }
