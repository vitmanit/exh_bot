from anyio.functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr
    db_url: SecretStr
    admins: SecretStr

    model_config = SettingsConfigDict(
        env_file='../.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()


config = get_settings()
