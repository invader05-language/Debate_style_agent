"""
Notifications API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from backend.database import get_db
from backend.models.notification import Notification

router = APIRouter()


@router.get("/notifications")
async def list_notifications(
    is_read: bool = None,
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db),
):
    """获取通知列表"""
    query = select(Notification)
    count_query = select(func.count(Notification.id))

    if is_read is not None:
        query = query.where(Notification.is_read == is_read)
        count_query = count_query.where(Notification.is_read == is_read)

    total = (await db.execute(count_query)).scalar() or 0
    query = query.order_by(Notification.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    notifications = result.scalars().all()

    unread_count = (await db.execute(
        select(func.count(Notification.id)).where(Notification.is_read == False)
    )).scalar() or 0

    return {
        "notifications": [
            {
                "id": str(n.id),
                "title": n.title,
                "message": n.message,
                "type": n.type,
                "is_read": n.is_read,
                "created_at": n.created_at.isoformat() if n.created_at else None,
            }
            for n in notifications
        ],
        "total": total,
        "unread_count": unread_count,
        "page": page,
        "page_size": page_size,
    }


@router.patch("/notifications/{notification_id}/read")
async def mark_read(
    notification_id: str,
    db: AsyncSession = Depends(get_db),
):
    """标记通知已读"""
    query = select(Notification).where(Notification.id == notification_id)
    result = await db.execute(query)
    notification = result.scalar_one_or_none()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    notification.is_read = True
    await db.commit()
    return {"id": str(notification.id), "is_read": True}


@router.post("/notifications/read-all")
async def mark_all_read(db: AsyncSession = Depends(get_db)):
    """标记所有通知已读"""
    query = select(Notification).where(Notification.is_read == False)
    result = await db.execute(query)
    for n in result.scalars().all():
        n.is_read = True
    await db.commit()
    return {"message": "All notifications marked as read"}
