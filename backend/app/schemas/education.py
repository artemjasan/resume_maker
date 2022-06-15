from pydantic import Field

from app.schemas.base_schemas import BaseModelWithDatesFiled


class EducationBase(BaseModelWithDatesFiled):
    name: str = Field(..., max_length=256)
    specialization: str = Field(..., max_length=256)
    description: str = Field(..., max_length=512)


class EducationCreate(EducationBase):
    pass


class EducationDB(EducationBase):
    id: str = ...
    profile_id: int = ...

    class Config:
        orm_mode = True
