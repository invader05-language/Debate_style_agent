"""
FAQ / Help Center API endpoints.
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel, Field
from backend.database import get_db
from backend.models.faq import FAQ

router = APIRouter()


class FAQCreate(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)
    answer: str = Field(..., min_length=1)
    category: Optional[str] = None
    sort_order: int = 0


class FAQUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    category: Optional[str] = None
    sort_order: Optional[int] = None


class FAQResponse(BaseModel):
    id: str
    question: str
    answer: str
    category: Optional[str] = None
    sort_order: int

    class Config:
        from_attributes = True


def _faq_to_response(f) -> FAQResponse:
    return FAQResponse(
        id=str(f.id),
        question=f.question,
        answer=f.answer,
        category=f.category,
        sort_order=f.sort_order or 0,
    )


@router.get("/faqs")
async def list_faqs(
    category: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """获取FAQ列表"""
    query = select(FAQ)
    if category:
        query = query.where(FAQ.category == category)
    query = query.order_by(FAQ.sort_order)
    result = await db.execute(query)
    faqs = result.scalars().all()

    # Group by category
    categories = {}
    for f in faqs:
        cat = f.category or "通用"
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(_faq_to_response(f))

    return {"faqs": [_faq_to_response(f) for f in faqs], "by_category": categories}


@router.post("/faqs", response_model=FAQResponse, status_code=201)
async def create_faq(
    body: FAQCreate,
    db: AsyncSession = Depends(get_db),
):
    """创建FAQ"""
    faq = FAQ(**body.dict())
    db.add(faq)
    await db.commit()
    await db.refresh(faq)
    return _faq_to_response(faq)


@router.patch("/faqs/{faq_id}", response_model=FAQResponse)
async def update_faq(
    faq_id: str,
    body: FAQUpdate,
    db: AsyncSession = Depends(get_db),
):
    """更新FAQ"""
    query = select(FAQ).where(FAQ.id == faq_id)
    result = await db.execute(query)
    faq = result.scalar_one_or_none()
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")

    for key, value in body.dict(exclude_unset=True).items():
        setattr(faq, key, value)

    await db.commit()
    await db.refresh(faq)
    return _faq_to_response(faq)


@router.delete("/faqs/{faq_id}", status_code=204)
async def delete_faq(
    faq_id: str,
    db: AsyncSession = Depends(get_db),
):
    """删除FAQ"""
    query = select(FAQ).where(FAQ.id == faq_id)
    result = await db.execute(query)
    faq = result.scalar_one_or_none()
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")

    await db.delete(faq)
    await db.commit()
