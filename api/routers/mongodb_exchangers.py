from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Dict
from app.bot import (  # ← Твой файл!
    add_site, get_sites, remove_site, get_all_exchangers, exchangers
)
from app.api.core.auth import get_current_admin

router = APIRouter(
    prefix="/admin/mongodb",
    tags=["MongoDB Exchangers"],
    responses={404: {"description": "Not found"}},
)


@router.get("/exchangers")
async def list_exchangers(
        admin: bool = Depends(get_current_admin)
) -> List[Dict]:
    """Получить все обменники с сайтами"""
    exchangers = await get_all_exchangers()
    return exchangers


@router.get("/exchangers/{exchange_name}/sites")
async def get_exchange_sites(
        exchange_name: str,
        admin: bool = Depends(get_current_admin)
) -> Dict[str, str]:
    """Сайты конкретного обменника"""
    sites = await get_sites(exchange_name)
    if not sites:
        raise HTTPException(404, f"Exchanger '{exchange_name}' not found")
    return sites


@router.post("/exchangers/{exchange_name}/sites/{site_name}")
async def add_exchange_site(
        exchange_name: str,
        site_name: str,
        url: str,
        admin: bool = Depends(get_current_admin)
) -> Dict:
    """Добавить/обновить сайт для обменника"""
    await add_site(exchange_name, site_name, url)
    return {"status": "ok", "exchange": exchange_name, "site": site_name, "url": url}


@router.delete("/exchangers/{exchange_name}/sites/{site_name}")
async def delete_exchange_site(
        exchange_name: str,
        site_name: str,
        confirm: bool = Query(False, description="Подтверждение удаления"),
        admin: bool = Depends(get_current_admin)
) -> Dict:
    """Удалить сайт обменника"""
    if not confirm:
        raise HTTPException(400, "Требуется ?confirm=true")

    await remove_site(exchange_name, site_name)
    return {"status": "deleted", "exchange": exchange_name, "site": site_name}


@router.get("/stats")
async def mongodb_stats(
        admin: bool = Depends(get_current_admin)
) -> Dict:
    """Статистика коллекции exchangers"""
    count = await exchangers.count_documents({})
    pipeline = [{"$group": {"_id": "$name", "sites_count": {"$size": "$sites"}}}]
    stats = await exchangers.aggregate(pipeline).to_list(None)
    return {"total_exchangers": count, "stats": stats}
