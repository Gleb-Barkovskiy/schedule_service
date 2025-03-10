import os

from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    db_url: str = os.getenv("DB_URL", f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3")
    db_echo: bool = False

    resource_url: str = os.getenv(
        "RESOURCE_URL", "https://mmf.bsu.by/ru/raspisanie-zanyatij/"
    )
    fetch_updates_interval: int = 12 * 60 * 60

    class Config:
        env_file = ".env"


settings = Settings()
