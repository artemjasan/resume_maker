from datetime import date, datetime

from pydantic import BaseModel, Field, validator

from app.schemas import education, experience, link, skill


class ProfileBase(BaseModel):
    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    middle_name: str = Field(..., max_length=50)
    birth_day: date = ...
    bio: str = Field(..., max_length=512)

    @validator("birth_day", pre=True)
    def validate_birth_day(cls, value):
        # TODO: Think about more clever and suitable way to validate birth day
        # Now its just for example
        if value > date.today():
            raise ValueError("Until date can't be without since")
        return value


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    links: list[link.LinkDB] = []
    educations: list[education.EducationDB] = []
    experiences: list[experience.ExperienceDB] = []
    skills: list[skill.SkillDB] = []
    updated_up: datetime


class ProfileDB(ProfileBase):
    id: int = ...
    user_id: int = ...
    links: list[link.LinkDB] = []
    educations: list[education.EducationDB] = []
    experiences: list[experience.ExperienceDB] = []
    skills: list[skill.SkillDB] = []
    created_at: datetime
    updated_up: datetime

    class Config:
        orm_mode = True
