from pydantic import Field

from app.schemas.base_schemas import BaseModelWithDatesFiled


class ExperienceBase(BaseModelWithDatesFiled):
    employer: str = Field(..., max_length=128)
    position: str = Field(..., max_length=128)
    description: str = Field(..., max_length=512)


class ExperienceCreate(ExperienceBase):
    pass


class ExperienceDB(ExperienceBase):
    id: str = ...
    profile_id: int = ...

    class Config:
        orm_mode = True
