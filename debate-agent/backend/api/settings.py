"""
Settings API endpoints.
"""

import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.database import get_db
from backend.models.settings import UserSettings

router = APIRouter()

DEFAULT_USER_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")


def _settings_to_dict(s: UserSettings) -> dict:
    return {
        "id": str(s.id),
        "user_id": str(s.user_id),
        "language": s.language,
        "theme_mode": s.theme_mode,
        "notifications": s.notifications,
        "weekly_digest": s.weekly_digest,
        "created_at": s.created_at.isoformat() if s.created_at else None,
        "updated_at": s.updated_at.isoformat() if s.updated_at else None,
    }


@router.get("/settings")
async def get_settings(
    db: AsyncSession = Depends(get_db),
):
    """获取用户设置"""
    query = select(UserSettings).where(UserSettings.user_id == DEFAULT_USER_ID)
    result = await db.execute(query)
    settings = result.scalar_one_or_none()

    if not settings:
        settings = UserSettings(user_id=DEFAULT_USER_ID)
        db.add(settings)
        await db.commit()
        await db.refresh(settings)

    return _settings_to_dict(settings)


@router.patch("/settings")
async def update_settings(
    body: dict,
    db: AsyncSession = Depends(get_db),
):
    """更新用户设置"""
    query = select(UserSettings).where(UserSettings.user_id == DEFAULT_USER_ID)
    result = await db.execute(query)
    settings = result.scalar_one_or_none()

    if not settings:
        settings = UserSettings(user_id=DEFAULT_USER_ID)
        db.add(settings)
        await db.commit()
        await db.refresh(settings)

    allowed_fields = {"language", "theme_mode", "notifications", "weekly_digest"}
    for key, value in body.items():
        if key in allowed_fields and hasattr(settings, key):
            setattr(settings, key, value)

    await db.commit()
    await db.refresh(settings)
    return _settings_to_dict(settings)
