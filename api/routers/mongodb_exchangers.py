from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Dict, Optional, Any

from pydantic import BaseModel

from api.schemas.mongo import Exchanger
from bot.mongo.mongo import (
    add_site, get_sites, remove_site, get_all_exchangers, exchangers
)
from api.core.auth import get_current_admin
from bot.mongo.mongo import db

router = APIRouter(
    prefix="/mongodb",
    tags=["MongoDB Exchangers"],
    responses={404: {"description": "Not found"}},
)


@router.get("/exchangers")
async def get_exchangers() -> List[Dict[str, Any]]:
    exchangers = await db.exchangers.find().to_list(length=1000)

    result = []
    for ex in exchangers:
        ex_copy = ex.copy()
        ex_copy["_id"] = str(ex["_id"])
        result.append(ex_copy)

    return result


@router.get("/exchangers/{exchange_name}/sites")
async def get_exchange_sites(
        exchange_name: str
):
    exchanger = await db.exchangers.find_one({"name": exchange_name})
    if not exchanger:
        raise HTTPException(status_code=404, detail="Exchange not found")

    sites = exchanger.get("sites", [])

    result = {"sites": sites, "exchange": exchange_name}
    return result


@router.post("/exchangers/{exchange_name}/sites/{site_name}")
async def add_exchange_site(
        exchange_name: str,
        site_name: str,
        url: str,
) -> Dict:
    """Добавить/обновить сайт для обменника"""
    await add_site(exchange_name, site_name, url)
    return {"status": "ok", "exchange": exchange_name, "site": site_name, "url": url}


@router.delete("/exchangers/{exchange_name}/sites/{site_name}")
async def delete_exchange_site(
        exchange_name: str,
        site_name: str,
        confirm: bool = Query(False, description="Подтверждение удаления"),
) -> Dict:
    """Удалить сайт обменника"""
    if not confirm:
        raise HTTPException(400, "Требуется ?confirm=true")

    await remove_site(exchange_name, site_name)
    return {"status": "deleted", "exchange": exchange_name, "site": site_name}