from pydantic import BaseModel, Field


class SkillBase(BaseModel):
    name: str = Field(..., max_length=64)
    proficiency: int = Field(default=None, ge=1, le=5, description="Your proficiency level")


class SkillCreate(SkillBase):
    pass


class SkillDB(SkillBase):
    id: str = ...
    profile_id: int = ...

    class Config:
        orm_mode = True
