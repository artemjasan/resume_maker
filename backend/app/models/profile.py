from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Date
from sqlalchemy.orm import relationship

from sqladmin import ModelAdmin

from .base import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="profiles")
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    middle_name = Column(String(50), nullable=True)
    birth_day = Column(Date, nullable=False)
    bio = Column(String(512), nullable=False)
    links = relationship("Link", back_populates="profile", cascade="all, delete-orphan", lazy="selectin")
    educations = relationship("Education", back_populates="profile", cascade="all, delete-orphan", lazy="selectin")
    experiences = relationship("Experience", back_populates="profile", cascade="all, delete-orphan", lazy="selectin")
    skills = relationship("Skill", back_populates="profile", cascade="all, delete-orphan", lazy="selectin")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class ProfileAdmin(ModelAdmin, model=Profile):
    column_list = [Profile.id, Profile.first_name, Profile.last_name, Profile.user_id]
