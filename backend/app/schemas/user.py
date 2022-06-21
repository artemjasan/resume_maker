from pydantic import BaseModel, EmailStr, Field

from app.schemas.profile import ProfileDB


class UserBase(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr = ...


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserDB(UserBase):
    id: int = ...
    profiles: list[ProfileDB] = []

    class Config:
        orm_mode = True
