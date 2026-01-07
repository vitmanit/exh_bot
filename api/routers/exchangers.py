import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.db import get_session
from bot.models.models import Exchanger
from api.schemas import ExchangerCreate, ExchangerResponse, ExchangerUpdate


router = APIRouter(prefix="/api/v1/exchangers", tags=["Exchangers"])


@router.get("/", response_model=List[ExchangerResponse])
async def list_exchangers(db: AsyncSession = Depends(get_session)):

    result = await db.execute(select(Exchanger))
    return result.scalars().all()


@router.get("/{exchanger_name}", response_model=ExchangerResponse)
async def get_exchanger(exc_name: str, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Exchanger).where(Exchanger.name == exc_name))
    exchangers = result.scalar_one_or_none()
    if exchangers is None:
        raise HTTPException(status_code=404, detail="Exchanger not found")
    return exchangers



@router.post("/create_exchangers", response_model=ExchangerCreate, status_code=201)
async def create_exchangers(exc_data: ExchangerCreate = Depends(), db: AsyncSession = Depends(get_session)):
    exchanger = Exchanger(**exc_data.model_dump())
    db.add(exchanger)
    await db.commit()
    await db.refresh(exchanger)
    return exchanger


@router.patch("/exchangers/{id}", response_model=ExchangerResponse)
async def update_exchanger(
        id: int,
        update_data: ExchangerUpdate = Depends(),
        db: AsyncSession = Depends(get_session)
):
    # Только изменённые и non-None поля
    update_dict = update_data.model_dump(exclude_unset=True, exclude_none=True)

    if not update_dict:  # Если ничего не передали
        raise HTTPException(status_code=400, detail="No fields to update")

    result = await db.execute(select(Exchanger).where(Exchanger.id == id))
    exchanger = result.scalar_one_or_none()
    if not exchanger:
        raise HTTPException(status_code=404, detail="Exchanger not found")

    for key, value in update_dict.items():
        setattr(exchanger, key, value)

    await db.commit()
    await db.refresh(exchanger)
    return exchanger


@router.delete("/exchangers/{id}", response_model=ExchangerResponse)
async def delete_exchanger(exchanger_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Exchanger).where(Exchanger.id == exchanger_id))
    exchanger = result.scalar_one_or_none()
    if not exchanger:
        raise HTTPException(404, "Exchanger not found")
    deleted_exchanger = exchanger
    await db.delete(exchanger)
    await db.commit()

    return deleted_exchanger



