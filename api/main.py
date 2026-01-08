from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from bot.database.db import engine
from bot.models import Base
from api.routers import exchangers, monitorings, plans
from api.routers import mongodb_exchangers



@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(title="ExchangeFeed API", lifespan=lifespan)


app.include_router(exchangers.router)
app.include_router(monitorings.router)
app.include_router(plans.router)
app.include_router(mongodb_exchangers.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



if __name__ == '__main__':
    try:
        uvicorn.run(
            "main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print('🔌 API остановлен пользователем')
