"""
Authentication schemas for JWT auth.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    """用户注册请求"""
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    """用户登录请求"""
    username: str
    password: str


class UserResponse(BaseModel):
    """用户信息响应"""
    id: str
    username: str
    email: str
    is_active: bool

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """JWT Token 响应"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
