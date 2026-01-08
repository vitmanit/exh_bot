from anyio.functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr
    db_url: SecretStr
    MONGO_ADMIN_TOKEN: SecretStr
    SECRET_KEY: SecretStr = SecretStr("your-super-secret-key-change-in-prod")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file='../.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()


config = get_settings()
