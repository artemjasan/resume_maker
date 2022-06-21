from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, delete, insert
from passlib.context import CryptContext

from app import models, schemas
from app.database.database import get_session
from app.core.config import settings

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/", response_model=list[schemas.UserDB])
async def read_users(session: AsyncSession = Depends(get_session)):
    q = await session.execute(select(models.User).order_by(models.User.id))
    users = q.scalars().all()
    return users


@router.post("/", response_model=schemas.UserDB)
async def create_user(user: schemas.UserCreate, session: AsyncSession = Depends(get_session)):
    # query = insert(models.User).values(
    #         username=user.username,
    #         email=user.email,
    #         hashed_password=pwd_context.encrypt(user.password)
    #     )
    new_user = models.User(
        username=user.username, email=user.email, hashed_password=pwd_context.encrypt(user.password)
    )
    session.add(new_user)
    try:
        await session.commit()
        return new_user
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="The user is already exist") from ex
