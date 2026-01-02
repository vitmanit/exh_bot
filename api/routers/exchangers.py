from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from bot.database.crud.exchanger import get_exchangers, create_exchanger
from bot.database.db import AsyncSessionLocal

router = APIRouter(prefix="/exchangers", tags=["exchangers"])

@router.get("/")
async def list_exchangers(session: AsyncSession = Depends(AsyncSessionLocal)):
    return await get_exchangers(session)

@router.post("/")
async def add_exchanger(exchanger_data: ExchangerCreate, session: AsyncSession = Depends(AsyncSessionLocal)):
    exchanger = Exchanger(**exchanger_data.dict())
    return await create_exchanger(exchanger, session)
