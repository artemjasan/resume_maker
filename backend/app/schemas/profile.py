import datetime

from pydantic import BaseModel, Field, validator

from app.schemas import education, experience, link, skill


class ProfileBase(BaseModel):
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    middle_name: str = Field(..., max_length=50)
    birth_day: datetime.date = Field(...)
    bio: str = Field(..., max_length=512)

    @validator("birth_day")
    def validate_birth_day(cls, value):
        # TODO: Think about more clever and suitable way to validate birth day
        if value >= datetime.date.today():
            raise ValueError("birth day can't be the today's date")
        return value


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    links: list[link.LinkDB] = []
    educations: list[education.EducationDB] = []
    experiences: list[experience.ExperienceDB] = []
    skills: list[skill.SkillDB] = []


class ProfileDB(ProfileBase):
    id: int = ...
    user_id: int = ...
    links: list[link.LinkDB] = []
    educations: list[education.EducationDB] = []
    experiences: list[experience.ExperienceDB] = []
    skills: list[skill.SkillDB] = []
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True
