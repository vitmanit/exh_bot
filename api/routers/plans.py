from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.db import get_session
from bot.models.models import Plan
from api.schemas import PlanCreate, PlanUpdate, PlanResponse

router = APIRouter(prefix="/api/v1", tags=["Plan"])


@router.get("/plans", response_model=List[PlanResponse], status_code=200)
async def get_plans(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Plan))
    return result.scalars().all()


@router.get("/plan/{plan_id}", response_model=PlanResponse, status_code=200)
async def get_plan(plan_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Plan).where(Plan.id == plan_id))
    plan = result.scalars().one_or_none()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan

@router.post("/plan", response_model=PlanCreate, status_code=201)
async def plan_create(plan: PlanCreate = Depends(), db: AsyncSession = Depends(get_session)):
    plan = Plan(**plan.model_dump())
    db.add(plan)
    await db.commit()
    await db.refresh(plan)
    return plan


@router.put("/plan/{plan_id}", response_model=PlanResponse, status_code=200)
async def update_plan(
        id: int,
        update_data: PlanUpdate = Depends(),
        db: AsyncSession = Depends(get_session)
):
    update_dict = update_data.model_dump(exclude_unset=True, exclude_none=True)

    if not update_dict:
        raise HTTPException(status_code=400, detail="No fields to update")

    result = await db.execute(select(Plan).where(Plan.id == id))
    plan = result.scalar_one_or_none()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    for key, value in update_dict.items():
        setattr(plan, key, value)

    await db.commit()
    await db.refresh(plan)
    return plan


@router.delete("/plan/{plan_id}", status_code=200)
async def delete_plan(plan_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Plan).where(Plan.id == plan_id))
    plan = result.scalar_one_or_none()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    deleted_plan = plan
    await db.delete(plan)
    await db.commit()
    return deleted_plan