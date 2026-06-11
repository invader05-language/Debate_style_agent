"""
Think engine Pydantic schemas.
"""

from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel, Field


class ThinkCreate(BaseModel):
    """Schema for creating a think session."""
    topic: str = Field(..., min_length=1, max_length=500, description="思考主题")
    depth: str = Field(default="standard", description="思考深度: quick/standard/deep")
    models: List[str] = Field(default_factory=lambda: ["mimo"], description="参与模型列表")
    config: Optional[Dict] = Field(default=None, description="额外配置")


class ThinkResponse(BaseModel):
    """Schema for think session response."""
    id: str
    topic: str
    status: str
    depth: Optional[str] = None
    created_at: Optional[str] = None
    completed_at: Optional[str] = None
    synthesis: Optional[str] = None
    insights: Optional[List[str]] = None
    messages: Optional[List["ThinkMessageResponse"]] = None

    class Config:
        from_attributes = True


class ThinkMessageResponse(BaseModel):
    """Schema for think message response."""
    id: str
    task_id: str
    model_id: Optional[str] = None
    role: str
    round_number: int
    content: str
    structured: Optional[Dict] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class ThinkListResponse(BaseModel):
    """Schema for think list response."""
    sessions: List[ThinkResponse]
    total: int
    page: int
    page_size: int
