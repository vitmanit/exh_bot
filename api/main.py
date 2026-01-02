from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.cors import CORSMiddleware

from bot.database.db import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: создание таблиц
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ База данных инициализирована")

    yield  # основной код API

    # Shutdown: закрытие engine
    await engine.dispose()
    print("🔌 БД закрыта")


app = FastAPI(title="ExchangeFeed API", lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(exchangers.router)
# app.include_router(monitorings.router)
# app.include_router(Plans.router)
#
# if  __name__ == '__main__':
#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         print('Бот выключен')
