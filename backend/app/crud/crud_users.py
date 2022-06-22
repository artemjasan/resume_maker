from typing import Any, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic.networks import EmailStr

from app.auth.users import get_password_hash, verify_password
from app.crud.crud_base import CRUDBase
from app.models.user import User
from app import schemas


class CRUDUser(CRUDBase[User, schemas.UserCreate, schemas.UserUpdate]):
    async def get_by_email(self, session: AsyncSession, email: str) -> User | None:
        response = await session.execute(select(self.model).where(self.model.email == email))
        return response.scalar_one()

    async def create(self, session: AsyncSession, obj_in: schemas.UserCreate) -> User:
        db_obj = User(
            username=obj_in.username,
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password)
        )
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self, session: AsyncSession, obj_current: User, obj_in: schemas.UserCreate | dict[str, Any]
    ) -> User:
        if isinstance(obj_in, dict):
            updated_data = obj_in
        else:
            updated_data = obj_in.dict(exclude_unset=True)
        if updated_data["password"]:
            hashed_password = get_password_hash(updated_data["password"])
            del updated_data["password"]
            updated_data["hashed_password"] = hashed_password
        # TODO: without await - typing warnings that it returns Coroutine [Any, Any, User]
        result = await super().update(session, obj_current, obj_in=updated_data)
        return result

    async def authenticate(self, session: AsyncSession, email: EmailStr, password: str) -> User | None:
        act_user = await self.get_by_email(session, email)
        if not user:
            return None
        if not verify_password(password, hashed_password=act_user.hashed_password):
            return None
        return act_user


user = CRUDUser(User)
