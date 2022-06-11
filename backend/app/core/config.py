import secrets

from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Resume Maker"
    PROJECT_VERSION: str = "0.1.0"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    SQL_ALCHEMY_DATA_BASE_URL: str = "sqlite:///../sqlite.db"


settings = Settings()
