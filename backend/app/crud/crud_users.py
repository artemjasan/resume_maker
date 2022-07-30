from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic.networks import EmailStr

from app.core.security import get_password_hash, verify_password
from app.crud.crud_base import CRUDBase
from app import models, schemas


class CRUDUser(CRUDBase[models.User, schemas.UserCreate, schemas.UserUpdate]):
    async def get_by_email(self, session: AsyncSession, email: str) -> models.User | None:
        response = await session.execute(select(self.model).where(self.model.email == email))
        return response.scalar()

    async def get_user_by_id(self, session: AsyncSession, id: int) -> models.User | None:
        return await super().get(session, id=id)

    async def create(self, session: AsyncSession, obj_in: schemas.UserCreate) -> models.User:
        db_obj = models.User(
            username=obj_in.username,
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            is_superuser=obj_in.is_superuser
        )
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self, session: AsyncSession, obj_current: models.User, obj_in: schemas.UserCreate | dict[str, Any]
    ) -> models.User:
        if isinstance(obj_in, dict):
            updated_data = obj_in
        else:
            updated_data = obj_in.dict(exclude_unset=True)
        if updated_data["password"]:
            hashed_password = get_password_hash(updated_data["password"])
            del updated_data["password"]
            updated_data["hashed_password"] = hashed_password
        result = await super().update(session, obj_current, obj_in=updated_data)
        return result

    async def authenticate(self, session: AsyncSession, email: EmailStr, password: str) -> models.User | None:
        act_user = await self.get_by_email(session, email)
        if not user:
            return None
        if not verify_password(password, hashed_password=act_user.hashed_password):
            return None
        return act_user

    def is_superuser(self, current_user: models.User) -> bool:
        return current_user.is_superuser


user = CRUDUser(models.User)
