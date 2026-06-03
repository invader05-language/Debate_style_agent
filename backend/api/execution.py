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
from execution.code_generator import CodeGenerator
from execution.sandbox import DockerSandbox, FallbackSandbox

router = APIRouter()


def _get_executor(use_sandbox: bool = True):
    """Get executor with optional sandbox."""
    if use_sandbox:
        try:
            return DockerSandbox()
        except Exception:
            return FallbackSandbox()
    return FallbackSandbox()


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


@router.post("/debates/{debate_id}/generate-code")
async def generate_code(
    debate_id: str,
    language: str = "python",
    db: AsyncSession = Depends(get_db)
):
    """从辩论结果生成代码"""
    from sqlalchemy import select

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

    # Generate code using AI
    from agents.mimo_agent import MIMOAgent
    generator = CodeGenerator(agent=MIMOAgent())
    generated = await generator.generate(debate.action_plan, language)

    return {
        "debate_id": debate_id,
        "language": language,
        "main_code": generated.main_code,
        "test_code": generated.test_code,
        "dependencies": generated.dependencies
    }


@router.post("/debates/{debate_id}/execute")
async def execute_debate(
    debate_id: str,
    use_sandbox: bool = True,
    db: AsyncSession = Depends(get_db)
):
    """执行辩论推荐方案"""
    from sqlalchemy import select

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

    # Execute code in background
    import asyncio
    asyncio.create_task(_execute_code(db, execution, use_sandbox))

    return {
        "id": str(execution.id),
        "debate_id": str(execution.debate_id),
        "status": execution.status,
        "message": "Execution started"
    }


@router.post("/executions/{execution_id}/retry")
async def retry_execution(
    execution_id: str,
    db: AsyncSession = Depends(get_db)
):
    """重试执行"""
    from sqlalchemy import select

    query = select(ExecutionModel).where(ExecutionModel.id == execution_id)
    result = await db.execute(query)
    execution = result.scalar_one_or_none()

    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")

    if execution.status not in ["failed", "success"]:
        raise HTTPException(status_code=400, detail="Can only retry failed or completed executions")

    # Reset status
    execution.status = "pending"
    execution.error_message = None
    execution.execution_result = None
    await db.commit()

    # Re-execute
    import asyncio
    asyncio.create_task(_execute_code(db, execution, True))

    return {
        "id": str(execution.id),
        "status": execution.status,
        "message": "Execution retry started"
    }


async def _execute_code(db: AsyncSession, execution: ExecutionModel,
                        use_sandbox: bool = True):
    """Execute code in background with retry logic."""
    from datetime import datetime
    import logging

    logger = logging.getLogger(__name__)
    max_retries = 3

    for attempt in range(max_retries):
        try:
            execution.status = "running"
            await db.commit()

            # Get executor
            executor = _get_executor(use_sandbox)

            # Execute code
            result = await executor.execute(execution.code_generated, "python")

            if result.success:
                execution.status = "success"
                execution.execution_result = result.output
                execution.error_message = None
                execution.completed_at = datetime.utcnow()
                await db.commit()
                return

            # If failed, try to refine code (except on last attempt)
            if attempt < max_retries - 1:
                logger.info(f"Execution failed, attempting refinement (attempt {attempt + 1})")
                from agents.mimo_agent import MIMOAgent
                from execution.code_generator import GeneratedCode

                generator = CodeGenerator(agent=MIMOAgent())
                code = GeneratedCode(main_code=execution.code_generated, language="python")
                refined = await generator.refine(code, result.error)
                execution.code_generated = refined.main_code
                continue

            # Final failure
            execution.status = "failed"
            execution.execution_result = result.output
            execution.error_message = result.error
            execution.completed_at = datetime.utcnow()
            await db.commit()

        except Exception as e:
            logger.error(f"Execution error: {e}")
            if attempt == max_retries - 1:
                execution.status = "failed"
                execution.error_message = str(e)
                execution.completed_at = datetime.utcnow()
                await db.commit()
            continue
