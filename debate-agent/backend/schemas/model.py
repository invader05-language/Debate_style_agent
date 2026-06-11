"""
AI Model management schemas.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ModelCreate(BaseModel):
    """Schema for creating an AI model."""
    name: str = Field(..., min_length=1, max_length=100)
    provider: str = Field(..., description="提供商: openai/anthropic/google/deepseek/mimo")
    model_id: str = Field(..., description="模型标识符，如 gpt-4o, claude-3-opus")
    api_url: str = Field(..., description="API地址")
    api_key: str = Field(..., description="API密钥")
    api_format: str = Field(default="openai", description="API格式: openai/anthropic/gemini")
    max_tokens: int = Field(default=4096, ge=1)
    temperature: float = Field(default=0.7, ge=0, le=2)
    is_preset: bool = Field(default=False)
    icon: Optional[str] = None
    color: Optional[str] = None


class ModelUpdate(BaseModel):
    """Schema for updating an AI model."""
    name: Optional[str] = None
    provider: Optional[str] = None
    model_id: Optional[str] = None
    api_url: Optional[str] = None
    api_key: Optional[str] = None
    api_format: Optional[str] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    is_active: Optional[bool] = None
    icon: Optional[str] = None
    color: Optional[str] = None


class ModelResponse(BaseModel):
    """Schema for model response."""
    id: str
    name: str
    provider: str
    model_id: str
    api_url: str
    api_format: str
    max_tokens: int
    temperature: float
    is_preset: bool
    is_active: bool
    icon: Optional[str] = None
    color: Optional[str] = None
    last_tested_at: Optional[str] = None
    last_test_status: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class ModelTestResponse(BaseModel):
    """Schema for model test result."""
    model_id: str
    status: str  # success / failed
    latency_ms: Optional[float] = None
    error: Optional[str] = None
    response_preview: Optional[str] = None


class ModelListResponse(BaseModel):
    """Schema for model list response."""
    models: list[ModelResponse]
    total: int
