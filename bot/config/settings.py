from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
env_file=BASE_DIR / ".env"

class Settings(BaseSettings):
    bot_token: SecretStr
    db_url: SecretStr
    admins: SecretStr

    model_config = SettingsConfigDict(env_file=str(env_file), env_file_encoding='utf-8', extra='ignore')


config = Settings()