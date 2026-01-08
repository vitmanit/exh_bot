import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from bot.config.settings import config
from api.core.jwt import get_password_hash
from bot.models.users import User
from bot.database.db import engine

async_session = async_sessionmaker(engine, expire_on_commit=False)

async def create_superadmin():
    async with async_session() as session:
        # Проверить по is_admin
        result = await session.execute(select(User).where(User.is_admin == True))
        admin = result.scalar_one_or_none()

        if admin:
            print("✅ Админ уже существует! ID:", admin.id)
            return

        # Создать суперадмина
        hashed_password = get_password_hash("admin123")
        new_admin = User(
            username="admin",  # ← username!
            hashed_password=hashed_password,
            is_active=True,
            is_admin=True
        )

        session.add(new_admin)
        await session.commit()
        await session.refresh(new_admin)
        print(f"✅ Суперадмин создан! ID: {new_admin.id}")
        print(f"👤 Логин: admin")
        print(f"🔑 Пароль: admin123")

if __name__ == "__main__":
    asyncio.run(create_superadmin())
