from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, delete, insert
from passlib.context import CryptContext

from app import models, schemas, crud
from app.database.database import get_session
from app.core.config import settings

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/", response_model=list[schemas.UserDB])
async def read_users(session: AsyncSession = Depends(get_session)):
    return await crud.user.get_multi(session=session)


@router.post("/", response_model=schemas.UserCreateResponse)
async def create_user(user: schemas.UserCreate, session: AsyncSession = Depends(get_session)):
    try:
        created_user = await crud.user.create(session=session, obj_in=user)
        return {"id": created_user.id, "username": created_user.username, "email": created_user.email}
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="The user is already exist."
        ) from ex
