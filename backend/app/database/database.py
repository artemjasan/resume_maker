from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core import config


engine = create_engine(
    # argument Check same thread just for SQLite,
    # see more in FastAPI tutorials: https://fastapi.tiangolo.com/tutorial/sql-databases/
    config.settings.SQL_ALCHEMY_DATA_BASE_URL, connect_arg={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
