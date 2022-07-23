from sqlalchemy import (Column, Integer, String, Boolean)
from sqlalchemy.orm import relationship
from sqladmin import ModelAdmin

from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    profiles = relationship("Profile", back_populates="user", cascade="all, delete-orphan", lazy="selectin")
    is_superuser = Column(Boolean(), default=False)


class UserAdmin(ModelAdmin, model=User):
    column_list = [User.id, User.username]
