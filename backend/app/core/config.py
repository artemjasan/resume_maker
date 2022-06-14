import secrets
import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    # Application
    PROJECT_NAME: str = "Resume Maker"
    PROJECT_VERSION: str = "0.1.0"
    # Secrets
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # DataBase
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres")
    SQL_ALCHEMY_DATA_BASE_URL: str = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}"


settings = Settings()
