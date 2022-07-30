from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud_base import CRUDBase
from app import models, schemas


class CRUDProfile(CRUDBase[models.Profile, schemas.ProfileCreate, schemas.ProfileUpdate]):
    async def create_with_user(
            self, session: AsyncSession, obj_in: schemas.ProfileCreate, user_id: int
    ) -> models.Profile:
        db_obj = models.Profile(
            **obj_in.dict(), user_id=user_id
        )
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_multi_profile_by_user(
            self, session: AsyncSession, user_id: int
    ) -> models.Profile:
        response = await session.execute(select(self.model).where(self.model.user_id == user_id))
        return response.scalars().all()


profile = CRUDProfile(models.Profile)
