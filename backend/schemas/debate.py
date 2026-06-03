"""
Debate Pydantic schemas for Multi-AI Debate Agent API.
"""

from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel, Field


class DebateCreate(BaseModel):
    """Schema for creating a new debate."""
    topic: str = Field(..., min_length=1, max_length=500, description="辩论主题")
    max_rounds: int = Field(default=3, ge=1, le=10, description="最大辩论轮次")
    models: Dict[str, str] = Field(
        default_factory=lambda: {"pro": "mimo", "con": "deepseek", "judge": "mimo"},
        description="模型配置"
    )


class MessageResponse(BaseModel):
    """Schema for message response."""
    id: str
    debate_id: str
    round_number: int
    role: str
    content: str
    model_used: str
    confidence: float
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class VerdictResponse(BaseModel):
    """Schema for verdict response."""
    recommendation: str
    winner: str
    confidence: float
    action_plan: List[str]


class DebateResponse(BaseModel):
    """Schema for debate response."""
    id: str
    topic: str
    status: str
    created_at: Optional[str] = None
    completed_at: Optional[str] = None
    verdict: Optional[VerdictResponse] = None
    action_plan: Optional[List[str]] = None
    messages: Optional[List[MessageResponse]] = None

    class Config:
        from_attributes = True


class DebateListResponse(BaseModel):
    """Schema for debate list response."""
    debates: List[DebateResponse]
    total: int
    page: int
    page_size: int
