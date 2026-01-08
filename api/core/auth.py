from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .jwt import SECRET_KEY, ALGORITHM, TokenData
from bot.database.db import get_session
from bot.models.users import User
from bot.config.settings import config


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    # Найти пользователя в БД
    result = await db.execute(select(User).where(User.username == token_data.username))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_admin(
        request: Request,  # ← ТВОЙ старый admin token
        current_user: User = Depends(get_current_active_user)
):
    # 1. Проверяем JWT (обычная авторизация)
    if current_user.is_admin:
        return current_user

    # 2. Проверяем старый admin token (для обратной совместимости)
    admin_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if admin_token == config.MONGO_ADMIN_TOKEN.get_secret_value():  # ← config!
        return {"is_admin": True}

    raise HTTPException(401, "Admin access required")