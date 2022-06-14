from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database.database import init_db


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION
)


# @app.on_event("startup")
# async def on_startup():
#     await init_db()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
