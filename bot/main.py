import asyncio
import logging
from bot.config.settings import config
from aiogram import Bot, Dispatcher
from bot.database import engine
from bot.models import Base
from bot.handlers import handlers
from aiogram.fsm.storage.memory import MemoryStorage
from bot.mongo import mongo


logging.basicConfig(level=logging.INFO)

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logging.info("✅ База данных инициализирована")

async def main():
    await init_models()

    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(handlers.router)

    await dp.start_polling(bot)

if  __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')