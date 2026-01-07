import asyncio
from typing import List, Dict, Optional
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://exchange_mongodb:27017/exchange_db")
db = client["exchange_db"]  # Измените с exchange_db на exchange (из вашего .env)
exchangers = db["exchangers"]


# Добавить/обновить сайт (ключ:значение)
async def add_site(exchange_name: str, site_name: str, url: str) -> None:
    await exchangers.update_one(
        {"name": exchange_name},
        {"$set": {f"sites.{site_name}": url}},
        upsert=True,
    )


# Получить все ссылки для обменника
async def get_sites(exchange_name: str) -> dict[str, str]:
    doc = await exchangers.find_one({"name": exchange_name})
    return doc.get("sites", {}) if doc else {}


# Удалить сайт
async def remove_site(exchange_name: str, site_name: str) -> None:
    await exchangers.update_one(
        {"name": exchange_name},
        {"$unset": {f"sites.{site_name}": ""}},
    )


# Получить все обменники с их сайтами
async def get_all_exchangers() -> list[dict]:
    cursor = exchangers.find({}, {"name": 1, "sites": 1})
    return await cursor.to_list(length=None)

# Обновить данные
async def update_site_url():
    pass