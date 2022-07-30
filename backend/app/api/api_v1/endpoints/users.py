from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from pydantic.networks import EmailStr

from app import models, schemas, crud
from app.api import dependencies
from app.database.database import get_session

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/list", response_model=list[schemas.UserDB])
async def read_users(session: AsyncSession = Depends(get_session)):
    return await crud.user.get_multi(session=session)


@router.post("/", response_model=schemas.UserCreateResponse)
async def create_user(user: schemas.UserCreate, session: AsyncSession = Depends(get_session)):
    try:
        created_user = await crud.user.create(session=session, obj_in=user)
        return created_user
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="The user is already exist."
        ) from ex


@router.put("/me", response_model=schemas.UserCreateResponse)
async def update_user_me(
        session: AsyncSession = Depends(get_session),
        password: str = Body(None),
        email: EmailStr = Body(None),
        current_user: models.User = Depends(dependencies.get_current_user)
):
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if email is not None:
        user_in.email = email
    user = await crud.user.update(session, obj_current=current_user, obj_in=user_in)
    return user


@router.get("/me", response_model=schemas.UserCreateResponse)
async def read_user_me(
        current_user: models.User = Depends(dependencies.get_current_user)
):
    return current_user


@router.get("/{user_id}", response_model=schemas.UserCreateResponse)
async def read_user_by_id(
        user_id: int,
        session: AsyncSession = Depends(get_session)
):
    user = await crud.user.get_user_by_id(session, id=user_id)
    return user


@router.put("/{user_id}", response_model=schemas.UserCreateResponse)
async def update_user(
        user_id: int,
        user_in: schemas.UserUpdate,
        session: AsyncSession = Depends(get_session),
        # current_user: models.User = Depends(deps.get_current_active_superuser),
):
    user = await crud.user.get(session=session, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )

    updated_user = await crud.user.update(session, obj_current=user, obj_in=user_in)
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user(
        user_id: int,
        session: AsyncSession = Depends(get_session),
        current_user: models.User = Depends(dependencies.get_current_user)
):
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Users can not delete theirselfs"
        )

    user = await crud.user.get_user_by_id(session=session, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User no found"
        )
    await crud.user.delete(session, id=user_id)
    return
