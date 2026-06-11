"""
Think engine API endpoints.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_db
from backend.schemas.think import ThinkCreate, ThinkResponse, ThinkMessageResponse, ThinkListResponse
from backend.services.think_service import ThinkService
from backend.models.task import Task
from backend.models.task_message import TaskMessage
from sqlalchemy import select

router = APIRouter()


def _task_to_response(task: Task, messages=None) -> ThinkResponse:
    """Convert Task model to ThinkResponse."""
    result = task.result or {}
    return ThinkResponse(
        id=str(task.id),
        topic=task.topic,
        status=task.status,
        depth=task.config.get("depth") if task.config else None,
        created_at=task.created_at.isoformat() if task.created_at else None,
        completed_at=task.completed_at.isoformat() if task.completed_at else None,
        synthesis=result.get("synthesis"),
        insights=result.get("insights"),
        messages=messages,
    )


@router.post("/think", response_model=ThinkResponse, status_code=201)
async def create_think_session(
    body: ThinkCreate,
    db: AsyncSession = Depends(get_db),
):
    """创建思考会话"""
    service = ThinkService(db)
    task = await service.create_session(
        topic=body.topic,
        depth=body.depth,
        models=body.models,
    )
    return _task_to_response(task)


@router.get("/think", response_model=ThinkListResponse)
async def list_think_sessions(
    page: int = 1,
    page_size: int = 10,
    db: AsyncSession = Depends(get_db),
):
    """获取思考会话列表"""
    service = ThinkService(db)
    sessions, total = await service.list_sessions(page=page, page_size=page_size)
    return ThinkListResponse(
        sessions=[_task_to_response(s) for s in sessions],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/think/{task_id}", response_model=ThinkResponse)
async def get_think_session(
    task_id: str,
    db: AsyncSession = Depends(get_db),
):
    """获取思考会话详情"""
    service = ThinkService(db)
    task = await service.get_session(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Think session not found")

    # Get messages
    msg_query = select(TaskMessage).where(TaskMessage.task_id == task_id).order_by(TaskMessage.round_number)
    msg_result = await db.execute(msg_query)
    messages_db = msg_result.scalars().all()

    messages = [
        ThinkMessageResponse(
            id=str(m.id),
            task_id=str(m.task_id),
            model_id=str(m.model_id) if m.model_id else None,
            role=m.role,
            round_number=m.round_number,
            content=m.content,
            structured=m.structured,
            created_at=m.created_at.isoformat() if m.created_at else None,
        )
        for m in messages_db
    ]

    return _task_to_response(task, messages=messages)


@router.post("/think/{task_id}/start", response_model=ThinkResponse)
async def start_think_session(
    task_id: str,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """启动思考会话（后台执行）"""
    service = ThinkService(db)
    task = await service.get_session(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Think session not found")
    if task.status != "pending":
        raise HTTPException(status_code=400, detail=f"Session is not pending (status: {task.status})")

    # Run in background
    from backend.database import AsyncSessionLocal

    async def _run():
        async with AsyncSessionLocal() as bg_db:
            bg_service = ThinkService(bg_db)
            await bg_service.run_session(task_id)

    background_tasks.add_task(_run)

    task.status = "running"
    await db.commit()

    return _task_to_response(task)
