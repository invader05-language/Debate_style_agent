"""
Authentication API endpoints for Multi-AI Debate Agent.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.database import get_db
from backend.models.user import UserModel
from backend.schemas.auth import UserCreate, UserLogin, UserResponse, TokenResponse
from backend.auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter()


@router.post("/auth/register", response_model=TokenResponse, status_code=201)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """用户注册"""
    # Check if username exists
    stmt = select(UserModel).where(UserModel.username == user_data.username)
    result = await db.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )

    # Check if email exists
    stmt = select(UserModel).where(UserModel.email == user_data.email)
    result = await db.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

    # Create user
    user = UserModel(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    # Generate token
    access_token = create_access_token(data={"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        user=UserResponse(
            id=str(user.id),
            username=user.username,
            email=user.email,
            is_active=user.is_active
        )
    )


@router.post("/auth/login", response_model=TokenResponse)
async def login(login_data: UserLogin, db: AsyncSession = Depends(get_db)):
    """用户登录"""
    # Find user by username
    stmt = select(UserModel).where(UserModel.username == login_data.username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )

    # Generate token
    access_token = create_access_token(data={"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        user=UserResponse(
            id=str(user.id),
            username=user.username,
            email=user.email,
            is_active=user.is_active
        )
    )


@router.get("/auth/me", response_model=UserResponse)
async def get_me(current_user: UserModel = Depends(get_current_user)):
    """获取当前用户信息"""
    return UserResponse(
        id=str(current_user.id),
        username=current_user.username,
        email=current_user.email,
        is_active=current_user.is_active
    )
