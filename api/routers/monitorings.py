from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.database.db import get_session
from app.models.models import Monitoring
from app.api.schemas.monitorings import *


router = APIRouter(prefix="/api/v1/monitoring", tags=["Monitoring"])


@router.get("/", response_model=List[MonitoringResponse], status_code=200)
async def list_monitoring(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Monitoring))
    return result.scalars().all()


@router.get("/{monitoring_id}", response_model=MonitoringResponse, status_code=200)
async def get_monitoring(monitoring_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Monitoring).where(Monitoring.id == monitoring_id))
    monitoring = result.scalar_one_or_none()
    if monitoring is None:
        raise HTTPException(status_code=404, detail="Monitoring not found")
    return monitoring



@router.post("/create_monitoring", response_model=MonitoringCreate)
async def create_monitoring(monitoring: MonitoringCreate = Depends(), db: AsyncSession = Depends(get_session)):
    monitoring = Monitoring(**monitoring.model_dump())
    db.add(monitoring)
    await db.commit()
    await db.refresh(monitoring)
    return monitoring


@router.patch("/monitoring/{id}", response_model=MonitoringResponse, status_code=200)
async def update_monitoring(
        id: int,
        update_data: MonitoringUpdate = Depends(),
        db: AsyncSession = Depends(get_session)
):
    update_dict = update_data.model_dump(exclude_unset=True, exclude_none=True)

    if not update_dict:
        raise HTTPException(status_code=400, detail="No fields to update")

    result = await db.execute(select(Monitoring).where(Monitoring.id == id))
    monitoring = result.scalar_one_or_none()
    if not monitoring:
        raise HTTPException(status_code=404, detail="Monitoring not found")

    for key, value in update_dict.items():
        setattr(monitoring, key, value)

    await db.commit()
    await db.refresh(monitoring)
    return monitoring

@router.delete("/monitoring/{id}", response_model=MonitoringResponse, status_code=200)
async def delete_exchanger(id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Monitoring).where(Monitoring.id == id))
    monitoring = result.scalar_one_or_none()
    if not monitoring:
        raise HTTPException(status_code=404, detail="Monitoring not found")
    delete_monitoring = monitoring
    await db.delete(monitoring)
    await db.commit()
    return delete_monitoring