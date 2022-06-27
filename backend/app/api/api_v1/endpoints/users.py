from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

from app import models, schemas, crud
from app.database.database import get_session
from app.core.config import settings

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/user/list", response_model=list[schemas.UserDB])
async def read_users(session: AsyncSession = Depends(get_session)):
    return await crud.user.get_multi(session=session)


@router.post("/user", response_model=schemas.UserCreateResponse)
async def create_user(user: schemas.UserCreate, session: AsyncSession = Depends(get_session)):
    try:
        created_user = await crud.user.create(session=session, obj_in=user)
        return {"id": created_user.id, "username": created_user.username, "email": created_user.email}
    except IntegrityError as ex:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="The user is already exist."
        ) from ex


@router.put("/user/{user_id}", response_model=schemas.UserCreateResponse)
async def update_user(
        user_id: int, user_in: schemas.UserUpdate,
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
    return {"id": updated_user.id, "username": updated_user.username, "email": updated_user.email}


@router.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    # current_user: User = Depends(deps.get_current_user(required_roles=[IRoleEnum.admin])),
):
    # if current_user.id == user_id:
    #     raise HTTPException(status_code=404, detail="Users can not delete theirselfs")

    user = await crud.user.get_user_by_id(session=session, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="The user with this id does not exist in the system")
    await crud.user.delete(session, id=user_id)
    return
