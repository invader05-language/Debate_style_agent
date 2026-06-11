"""
AI Model management API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_db
from backend.schemas.model import (
    ModelCreate, ModelUpdate, ModelResponse, ModelTestResponse, ModelListResponse,
)
from backend.services.model_service import ModelService

router = APIRouter()


def _model_to_response(m) -> ModelResponse:
    return ModelResponse(
        id=str(m.id),
        name=m.name,
        provider=m.provider,
        model_id=m.model_id,
        api_url=m.api_url,
        api_format=m.api_format,
        max_tokens=m.max_tokens,
        temperature=m.temperature,
        is_preset=m.is_preset,
        is_active=m.is_active,
        icon=m.icon,
        color=m.color,
        last_tested_at=m.last_tested_at.isoformat() if m.last_tested_at else None,
        last_test_status=m.last_test_status,
        created_at=m.created_at.isoformat() if m.created_at else None,
    )


@router.get("/models", response_model=ModelListResponse)
async def list_models(
    include_inactive: bool = False,
    db: AsyncSession = Depends(get_db),
):
    """获取AI模型列表"""
    service = ModelService(db)
    models = await service.list_models(include_inactive=include_inactive)
    return ModelListResponse(
        models=[_model_to_response(m) for m in models],
        total=len(models),
    )


@router.post("/models", response_model=ModelResponse, status_code=201)
async def create_model(
    body: ModelCreate,
    db: AsyncSession = Depends(get_db),
):
    """创建AI模型"""
    service = ModelService(db)
    model = await service.create_model(**body.dict())
    return _model_to_response(model)


@router.get("/models/{model_id}", response_model=ModelResponse)
async def get_model(
    model_id: str,
    db: AsyncSession = Depends(get_db),
):
    """获取AI模型详情"""
    service = ModelService(db)
    model = await service.get_model(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return _model_to_response(model)


@router.patch("/models/{model_id}", response_model=ModelResponse)
async def update_model(
    model_id: str,
    body: ModelUpdate,
    db: AsyncSession = Depends(get_db),
):
    """更新AI模型"""
    service = ModelService(db)
    model = await service.update_model(model_id, **body.dict(exclude_unset=True))
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    return _model_to_response(model)


@router.delete("/models/{model_id}", status_code=204)
async def delete_model(
    model_id: str,
    db: AsyncSession = Depends(get_db),
):
    """删除AI模型"""
    service = ModelService(db)
    deleted = await service.delete_model(model_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Model not found")


@router.post("/models/{model_id}/test", response_model=ModelTestResponse)
async def test_model(
    model_id: str,
    db: AsyncSession = Depends(get_db),
):
    """测试AI模型连接"""
    service = ModelService(db)
    result = await service.test_model(model_id)
    if result.get("error") == "Model not found":
        raise HTTPException(status_code=404, detail="Model not found")
    return ModelTestResponse(**result)
