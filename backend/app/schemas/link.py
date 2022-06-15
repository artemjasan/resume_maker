from enum import Enum
from pydantic import BaseModel, HttpUrl, Field


class LinkType(str, Enum):
    facebook = "Facebook"
    linkedin = "LinkedIn"
    instagram = "Instagram"
    github = "GitHub"


class LinkBase(BaseModel):
    name: LinkType = Field(..., max_length=64)
    url: HttpUrl = Field(..., description="URL link to the social media source")


class LinkCreate(LinkBase):
    pass


class LinkDB(LinkBase):
    id: str = ...
    profile_id: int = ...

    class Config:
        orm_mode = True
