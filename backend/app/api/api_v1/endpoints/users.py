from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, delete, insert
from passlib.context import CryptContext

from app import models, schemas
from app.database.database import get_session
from app.core.config import settings
from app.crud import users

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/", response_model=list[schemas.UserDB])
async def read_users(session: AsyncSession = Depends(get_session)):
    query = await session.execute(select(models.User).order_by(models.User.id))
    users = query.scalars().all()
    return users


@router.post("/", response_model=schemas.UserCreateResponse)
async def create_user(user: schemas.UserCreate, session: AsyncSession = Depends(get_session)):
    created_user = await users.create_user(session=session, user=user)
    try:
        await session.commit()
        return {"id": created_user.id, "username": created_user.username, "email": created_user.email}
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="The user is already exist."
        ) from ex
