"""
Execution API endpoints for Multi-AI Debate Agent.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_db
from backend.models.execution import ExecutionModel
from backend.models.debate import DebateModel
from execution.executor import CodeExecutor

router = APIRouter()


class ExecutionResponse:
    """Schema for execution response."""
    def __init__(self, id, debate_id, status, code_generated,
                 execution_result, error_message, created_at, completed_at):
        self.id = id
        self.debate_id = debate_id
        self.status = status
        self.code_generated = code_generated
        self.execution_result = execution_result
        self.error_message = error_message
        self.created_at = created_at
        self.completed_at = completed_at


@router.get("/executions/{execution_id}")
async def get_execution(
    execution_id: str,
    db: AsyncSession = Depends(get_db)
):
    """获取执行结果"""
    from sqlalchemy import select
    query = select(ExecutionModel).where(ExecutionModel.id == execution_id)
    result = await db.execute(query)
    execution = result.scalar_one_or_none()

    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")

    return {
        "id": str(execution.id),
        "debate_id": str(execution.debate_id),
        "status": execution.status,
        "code_generated": execution.code_generated,
        "execution_result": execution.execution_result,
        "error_message": execution.error_message,
        "created_at": execution.created_at.isoformat() if execution.created_at else None,
        "completed_at": execution.completed_at.isoformat() if execution.completed_at else None
    }


@router.post("/debates/{debate_id}/execute")
async def execute_debate(
    debate_id: str,
    db: AsyncSession = Depends(get_db)
):
    """执行辩论推荐方案"""
    from sqlalchemy import select
    from datetime import datetime

    # Get debate
    query = select(DebateModel).where(DebateModel.id == debate_id)
    result = await db.execute(query)
    debate = result.scalar_one_or_none()

    if not debate:
        raise HTTPException(status_code=404, detail="Debate not found")

    if debate.status != "completed":
        raise HTTPException(status_code=400, detail="Debate not completed")

    if not debate.action_plan:
        raise HTTPException(status_code=400, detail="No action plan available")

    # Create execution record
    execution = ExecutionModel(
        debate_id=debate.id,
        status="pending",
        code_generated="\n".join(debate.action_plan)
    )
    db.add(execution)
    await db.commit()
    await db.refresh(execution)

    # Execute code
    import asyncio
    asyncio.create_task(_execute_code(db, execution))

    return {
        "id": str(execution.id),
        "debate_id": str(execution.debate_id),
        "status": execution.status,
        "message": "Execution started"
    }


async def _execute_code(db: AsyncSession, execution: ExecutionModel):
    """Execute code in background."""
    from datetime import datetime

    try:
        execution.status = "running"
        await db.commit()

        # Execute code
        executor = CodeExecutor()
        result = await executor.execute(execution.code_generated, "python")

        # Update execution record
        execution.status = "success" if result.success else "failed"
        execution.execution_result = result.output
        execution.error_message = result.error
        execution.completed_at = datetime.utcnow()

        await db.commit()

    except Exception as e:
        execution.status = "failed"
        execution.error_message = str(e)
        execution.completed_at = datetime.utcnow()
        await db.commit()
