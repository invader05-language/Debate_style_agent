"""
Execution API endpoints for Multi-AI Debate Agent.
Handles code generation from debate results and sandbox execution.
"""

import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from backend.database import get_db
from backend.models.execution import ExecutionModel
from backend.models.debate import DebateModel
from execution.executor import CodeExecutor

logger = logging.getLogger(__name__)

router = APIRouter()


# ── Request / Response schemas ───────────────────────────────────

class GenerateCodeRequest(BaseModel):
    """Request body for generate-code endpoint."""
    language: str = "python"
    max_retries: int = 3
    use_sandbox: bool = True


# ── Endpoints ────────────────────────────────────────────────────

@router.get("/executions/{execution_id}")
async def get_execution(
    execution_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get execution result by ID."""
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
        "completed_at": execution.completed_at.isoformat() if execution.completed_at else None,
    }


@router.post("/debates/{debate_id}/generate-code")
async def generate_and_execute(
    debate_id: str,
    request: GenerateCodeRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """
    Generate code from debate action_plan and execute in sandbox.

    Flow:
    1. Fetch debate verdict + action_plan
    2. AI generates executable code
    3. Execute in Docker sandbox (or local fallback)
    4. Auto-retry with AI fix on failure
    """
    query = select(DebateModel).where(DebateModel.id == debate_id)
    result = await db.execute(query)
    debate = result.scalar_one_or_none()

    if not debate:
        raise HTTPException(status_code=404, detail="Debate not found")

    if debate.status != "completed":
        raise HTTPException(
            status_code=409,
            detail=f"Debate status is '{debate.status}', must be 'completed'"
        )

    if not debate.action_plan:
        raise HTTPException(status_code=409, detail="No action plan available")

    # Create execution record
    execution = ExecutionModel(
        debate_id=debate.id,
        status="pending",
        code_generated="",
    )
    db.add(execution)
    await db.commit()
    await db.refresh(execution)

    # Run generation + execution in background
    background_tasks.add_task(
        _run_generate_and_execute,
        execution_id=str(execution.id),
        action_plan=debate.action_plan,
        language=request.language,
        max_retries=request.max_retries,
        use_sandbox=request.use_sandbox,
    )

    logger.info(
        f"Started code generation for debate {debate_id}, "
        f"execution {execution.id}"
    )

    return {
        "id": str(execution.id),
        "debate_id": str(execution.debate_id),
        "status": "pending",
        "message": "Code generation and execution started",
    }


@router.post("/debates/{debate_id}/execute")
async def execute_debate(
    debate_id: str,
    background_tasks: BackgroundTasks,
    use_sandbox: bool = True,
    db: AsyncSession = Depends(get_db)
):
    """
    Execute debate action_plan directly (legacy).
    Joins action_plan steps as text and runs them.
    For AI-powered generation, use /generate-code instead.
    """
    query = select(DebateModel).where(DebateModel.id == debate_id)
    result = await db.execute(query)
    debate = result.scalar_one_or_none()

    if not debate:
        raise HTTPException(status_code=404, detail="Debate not found")

    if debate.status != "completed":
        raise HTTPException(status_code=400, detail="Debate not completed")

    if not debate.action_plan:
        raise HTTPException(status_code=400, detail="No action plan available")

    execution = ExecutionModel(
        debate_id=debate.id,
        status="pending",
        code_generated="\n".join(debate.action_plan),
    )
    db.add(execution)
    await db.commit()
    await db.refresh(execution)

    background_tasks.add_task(
        _run_direct_execution,
        execution_id=str(execution.id),
        code=execution.code_generated,
        use_sandbox=use_sandbox,
    )

    return {
        "id": str(execution.id),
        "debate_id": str(execution.debate_id),
        "status": "pending",
        "message": "Execution started",
    }


@router.post("/executions/{execution_id}/retry")
async def retry_execution(
    execution_id: str,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """Retry a failed execution."""
    query = select(ExecutionModel).where(ExecutionModel.id == execution_id)
    result = await db.execute(query)
    execution = result.scalar_one_or_none()

    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")

    if execution.status not in ["failed", "success"]:
        raise HTTPException(
            status_code=400,
            detail="Can only retry failed or completed executions"
        )

    execution.status = "pending"
    execution.error_message = None
    execution.execution_result = None
    execution.completed_at = None
    await db.commit()

    background_tasks.add_task(
        _run_direct_execution,
        execution_id=str(execution.id),
        code=execution.code_generated,
        use_sandbox=True,
    )

    return {
        "id": str(execution.id),
        "status": "pending",
        "message": "Execution retry started",
    }


@router.get("/debates/{debate_id}/executions")
async def list_executions(
    debate_id: str,
    db: AsyncSession = Depends(get_db)
):
    """List all executions for a debate."""
    query = (
        select(ExecutionModel)
        .where(ExecutionModel.debate_id == debate_id)
        .order_by(ExecutionModel.created_at.desc())
    )
    result = await db.execute(query)
    executions = result.scalars().all()

    return [
        {
            "id": str(ex.id),
            "debate_id": str(ex.debate_id),
            "status": ex.status,
            "code_generated": ex.code_generated,
            "execution_result": ex.execution_result,
            "error_message": ex.error_message,
            "created_at": ex.created_at.isoformat() if ex.created_at else None,
            "completed_at": ex.completed_at.isoformat() if ex.completed_at else None,
        }
        for ex in executions
    ]


# ── Background tasks ─────────────────────────────────────────────

async def _run_generate_and_execute(
    execution_id: str,
    action_plan: List[str],
    language: str,
    max_retries: int,
    use_sandbox: bool,
):
    """Background: generate code from action_plan, execute with auto-fix."""
    from backend.database import AsyncSessionLocal

    async with AsyncSessionLocal() as db:
        try:
            query = select(ExecutionModel).where(ExecutionModel.id == execution_id)
            result = await db.execute(query)
            execution = result.scalar_one_or_none()

            if not execution:
                logger.error(f"Execution {execution_id} not found")
                return

            execution.status = "running"
            await db.commit()

            executor = CodeExecutor(use_sandbox=use_sandbox)
            exec_result = await executor.generate_and_execute(
                action_plan=action_plan,
                language=language,
                max_retries=max_retries,
            )

            execution.status = "success" if exec_result.success else "failed"
            execution.execution_result = exec_result.output
            execution.error_message = (
                exec_result.error if not exec_result.success else ""
            )
            execution.completed_at = datetime.utcnow()
            await db.commit()

            logger.info(
                f"Execution {execution_id} finished: status={execution.status}"
            )

        except Exception as e:
            logger.exception(f"Execution {execution_id} crashed: {e}")
            try:
                execution.status = "failed"
                execution.error_message = str(e)
                execution.completed_at = datetime.utcnow()
                await db.commit()
            except Exception:
                pass


async def _run_direct_execution(
    execution_id: str,
    code: str,
    use_sandbox: bool = True,
):
    """Background: execute code directly, retry with AI fix on failure."""
    from backend.database import AsyncSessionLocal
    from execution.code_generator import CodeGenerator, GeneratedCode
    from agents.mimo_agent import MIMOAgent

    async with AsyncSessionLocal() as db:
        max_retries = 3

        try:
            query = select(ExecutionModel).where(ExecutionModel.id == execution_id)
            result = await db.execute(query)
            execution = result.scalar_one_or_none()

            if not execution:
                return

            execution.status = "running"
            await db.commit()

            executor = CodeExecutor(use_sandbox=use_sandbox)

            for attempt in range(max_retries):
                exec_result = await executor.execute(code, "python")

                if exec_result.success:
                    execution.status = "success"
                    execution.execution_result = exec_result.output
                    execution.error_message = None
                    execution.completed_at = datetime.utcnow()
                    await db.commit()
                    return

                # On failure: try AI fix (except last attempt)
                if attempt < max_retries - 1:
                    logger.info(
                        f"Execution {execution_id} failed, "
                        f"AI fix attempt {attempt + 1}"
                    )
                    generator = CodeGenerator(agent=MIMOAgent())
                    gen_code = GeneratedCode(main_code=code, language="python")
                    refined = await generator.refine(gen_code, exec_result.error)
                    code = refined.main_code
                    execution.code_generated = code
                    await db.commit()
                    continue

                # Final failure
                execution.status = "failed"
                execution.execution_result = exec_result.output
                execution.error_message = exec_result.error
                execution.completed_at = datetime.utcnow()
                await db.commit()

        except Exception as e:
            logger.exception(f"Direct execution {execution_id} crashed: {e}")
            try:
                execution.status = "failed"
                execution.error_message = str(e)
                execution.completed_at = datetime.utcnow()
                await db.commit()
            except Exception:
                pass
