"""
Memory Pydantic schemas for Multi-AI Debate Agent API.
"""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class MemoryCreate(BaseModel):
    """Schema for creating a new memory."""
    topic: str = Field(..., min_length=1, max_length=500, description="主题")
    debate_summary: str = Field(..., description="辩论总结")
    outcome: Optional[str] = Field(None, description="结果")
    confidence: float = Field(default=0.5, ge=0.0, le=1.0, description="信心度")
    tags: List[str] = Field(default_factory=list, description="标签")
    lessons_learned: List[str] = Field(default_factory=list, description="经验教训")


class MemoryResponse(BaseModel):
    """Schema for memory response."""
    id: str
    topic: str
    debate_summary: str
    outcome: Optional[str] = None
    confidence: float
    tags: List[str]
    lessons_learned: List[str]
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class MemorySearchResponse(BaseModel):
    """Schema for memory search response."""
    memories: List[MemoryResponse]
    total: int
    query: str


class MemoryUpdate(BaseModel):
    """Schema for updating a memory."""
    topic: Optional[str] = Field(None, max_length=500)
    debate_summary: Optional[str] = None
    outcome: Optional[str] = None
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    tags: Optional[List[str]] = None
    lessons_learned: Optional[List[str]] = None
