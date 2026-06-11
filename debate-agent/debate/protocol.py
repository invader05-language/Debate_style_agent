"""
Debate protocol definitions for Multi-AI Debate Agent.
Defines the structure and rules of the debate process.
"""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class DebateStatus(str, Enum):
    """Debate status enum."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    EXECUTED = "executed"
    FAILED = "failed"


class Role(str, Enum):
    """Debate role enum."""
    PRO = "pro"
    CON = "con"
    JUDGE = "judge"


class Message(BaseModel):
    """Debate message model."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    debate_id: str
    round_number: int
    role: Role
    content: str
    model_used: str
    confidence: float = Field(ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=datetime.now)


class Round(BaseModel):
    """Debate round model."""
    round_number: int
    pro_message: Message
    con_message: Message
    judge_message: Optional[Message] = None


class Verdict(BaseModel):
    """Debate verdict model."""
    recommendation: str
    winner: str = Field(pattern="^(pro|con|draw)$")
    confidence: float = Field(ge=0.0, le=1.0)
    action_plan: List[str]


class DebateResult(BaseModel):
    """Debate result model."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    topic: str
    status: DebateStatus
    rounds: List[Round]
    verdict: Optional[Verdict] = None
    created_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None


class DebateConfig(BaseModel):
    """Debate configuration."""
    topic: str
    max_rounds: int = 3
    timeout: int = 300  # seconds
    models: dict = Field(default_factory=lambda: {
        "pro": "mimo",
        "con": "deepseek",
        "judge": "mimo"
    })
