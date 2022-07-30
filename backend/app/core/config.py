import secrets
import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    # Application
    PROJECT_NAME: str = "Resume Maker"
    PROJECT_VERSION: str = "0.1.0"
    # Main Api path
    API_V1_STR: str = "/api/v1"
    # Secrets
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM = "HS256"
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # 30 minutes now, for dev period
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 30
    # DataBase
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres")
    SQL_ALCHEMY_DATA_BASE_URL: str = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}"
    # App constants
    MAX_USER_PROFILES: int = 3


settings = Settings()
