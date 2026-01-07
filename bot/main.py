import asyncio
import logging
from typing import Any

from faststream.rabbit.fastapi import RabbitBroker

from config.settings import config
from aiogram import Bot, Dispatcher
from database import engine
from models import Base
from handlers import handlers
from aiogram.fsm.storage.memory import MemoryStorage
from mongo import mongo

broker = RabbitBroker()

logging.basicConfig(level=logging.INFO)

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logging.info("✅ База данных инициализирована")


# @broker.subscriber("exchangers")
# async def exchangers_consumer(msg: dict | Any):
#     print(f"{msg}")
#     try:
#         await bot.send_message(
#             chat_id=342206495,
#             text=f"{msg}"
#         )
#     except Exception as e:
#         logging.error(f"Telegram error: {e}")

async def main():
    await init_models()
    # global bot
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(handlers.router)


    # async with broker:
    #     logging.info("🐰 Брокер запущен")
    #     logging.info("🤖 Telegram bot запущен")
    #
    #     await asyncio.gather(
    #         broker.start(),
    #         dp.start_polling(bot)
    #     )

if  __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')