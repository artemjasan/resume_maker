from pydantic import BaseModel, EmailStr, Field

from app.schemas.profile import ProfileDB


class UserBase(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr = ...


class UserDB(UserBase):
    id: int = ...
    profiles: list[ProfileDB] = []

    class Config:
        orm_mode = True


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


# Properties to receive via API on creation as response
class UserCreateResponse(UserBase):
    id: int = Field(...)


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: str | None = Field(default=None, min_length=8)
