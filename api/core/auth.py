from fastapi import Request, HTTPException, Depends
from bot.config.settings import config

async def get_current_admin(request: Request):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if token != config.MONGO_ADMIN_TOKEN:
        raise HTTPException(401, "Admin token required")
    return True
