from sqlalchemy import select
from bot.database import AsyncSessionLocal
from bot.models.models import Exchanger

async def get_exchangers():
    async with AsyncSessionLocal() as session:
        stmt = select(Exchanger)
        result = await session.execute(stmt)
        return result.scalars().all()

async def get_exchanger_by_id(exchanger_id: int):
    async with AsyncSessionLocal() as session:
        stmt = select(Exchanger).where(Exchanger.id == exchanger_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

async def create_exchanger(exchanger: Exchanger):
    async with AsyncSessionLocal() as session:
        session.add(exchanger)
        await session.commit()
        await session.refresh(exchanger)
        return exchanger
