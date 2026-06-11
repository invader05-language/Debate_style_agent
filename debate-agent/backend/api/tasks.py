"""
Tasks / History API endpoints — unified task history for all task types.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from backend.database import get_db
from backend.models.task import Task
from backend.models.task_message import TaskMessage

router = APIRouter()


@router.get("/tasks")
async def list_tasks(
    type: Optional[str] = Query(default=None, description="任务类型: debate/think"),
    status: Optional[str] = Query(default=None, description="任务状态"),
    page: int = 1,
    page_size: int = 20,
    db: AsyncSession = Depends(get_db),
):
    """获取任务列表（历史记录）"""
    query = select(Task)
    count_query = select(func.count(Task.id))

    if type:
        query = query.where(Task.type == type)
        count_query = count_query.where(Task.type == type)
    if status:
        query = query.where(Task.status == status)
        count_query = count_query.where(Task.status == status)

    # Total count
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # Paginated results
    query = query.order_by(Task.created_at.desc()).offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    tasks = result.scalars().all()

    return {
        "tasks": [
            {
                "id": str(t.id),
                "type": t.type,
                "topic": t.topic,
                "status": t.status,
                "config": t.config,
                "result": t.result,
                "created_at": t.created_at.isoformat() if t.created_at else None,
                "completed_at": t.completed_at.isoformat() if t.completed_at else None,
            }
            for t in tasks
        ],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.get("/tasks/{task_id}")
async def get_task(
    task_id: str,
    db: AsyncSession = Depends(get_db),
):
    """获取任务详情"""
    query = select(Task).where(Task.id == task_id)
    result = await db.execute(query)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Get messages
    msg_query = (
        select(TaskMessage)
        .where(TaskMessage.task_id == task_id)
        .order_by(TaskMessage.round_number)
    )
    msg_result = await db.execute(msg_query)
    messages = msg_result.scalars().all()

    return {
        "id": str(task.id),
        "type": task.type,
        "topic": task.topic,
        "status": task.status,
        "config": task.config,
        "result": task.result,
        "created_at": task.created_at.isoformat() if task.created_at else None,
        "completed_at": task.completed_at.isoformat() if task.completed_at else None,
        "messages": [
            {
                "id": str(m.id),
                "model_id": str(m.model_id) if m.model_id else None,
                "role": m.role,
                "round_number": m.round_number,
                "content": m.content,
                "structured": m.structured,
                "created_at": m.created_at.isoformat() if m.created_at else None,
            }
            for m in messages
        ],
    }


@router.delete("/tasks/{task_id}", status_code=204)
async def delete_task(
    task_id: str,
    db: AsyncSession = Depends(get_db),
):
    """删除任务"""
    query = select(Task).where(Task.id == task_id)
    result = await db.execute(query)
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Delete associated messages first
    msg_query = select(TaskMessage).where(TaskMessage.task_id == task_id)
    msg_result = await db.execute(msg_query)
    for msg in msg_result.scalars().all():
        await db.delete(msg)

    await db.delete(task)
    await db.commit()
