from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app import models, schemas, crud
from app.services import profile_services
from app.core.config import settings
from app.api import dependencies
from app.database.database import get_session

router = APIRouter()


@router.get("/", response_model=List[schemas.ProfileDB])
async def read_profiles(
        session: AsyncSession = Depends(get_session),
        current_user: models.User = Depends(dependencies.get_current_user)
):
    if crud.user.is_superuser(current_user=current_user):
        profiles = await crud.profile.get_multi(session=session)
    else:
        profiles = await crud.profile.get_multi_profile_by_user(session=session, user_id=current_user.id)
    return profiles


@router.post("/", response_model=schemas.ProfileDB)
async def create_profile(
        profile_in: schemas.ProfileCreate,
        session: AsyncSession = Depends(get_session),
        current_user: models.User = Depends(dependencies.get_current_user)
):
    if not profile_services.check_profiles_number(current_user=current_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"You can't create more than {settings.MAX_USER_PROFILES} profiles for one user."
        )
    profile = await crud.profile.create_with_user(session=session, obj_in=profile_in, user_id=current_user.id)
    return profile


@router.get("/{id}", response_model=schemas.ProfileDB)
async def read_profile(
        id: int,
        session: AsyncSession = Depends(get_session),
        current_user: models.User = Depends(dependencies.get_current_user)
):
    profile = await crud.profile.get(session=session, id=id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    if not crud.user.is_superuser(current_user=current_user) and (profile.user_id != current_user.id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The user hasn't enough permission")
    return profile


@router.put("/{id}", response_model=schemas.ProfileDB)
async def update_profile(
        id: int,
        profile_in: schemas.ProfileUpdate,
        session: AsyncSession = Depends(get_session),
        current_user: models.User = Depends(dependencies.get_current_user)
):
    profile = await crud.profile.get(session=session, id=id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    if not crud.user.is_superuser(current_user=current_user) and (profile.user_id != current_user.id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The user hasn't enough permission")
    profile = await crud.profile.update(session=session, obj_current=profile, obj_in=profile_in)
    return profile


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(
        id: int,
        session: AsyncSession = Depends(get_session),
        current_user: models.User = Depends(dependencies.get_current_user)
):
    profile = await crud.profile.get(session=session, id=id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    if not crud.user.is_superuser(current_user=current_user) and (profile.user_id != current_user.id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The user hasn't enough permission")
    await crud.profile.delete(session=session, id=id)
    return
