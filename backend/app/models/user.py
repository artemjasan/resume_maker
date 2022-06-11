from sqlalchemy import (Column, ForeignKey, Integer, String, DateTime, Date)
from sqlalchemy.orm import relationship

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    profiles = relationship("Profile", back_populates="user", cascade="all, delete-orphan")
    # Need more information how to implement them in pydantic schemas. I'll add it later.
    # created_at = Column(DateTime, default=datetime.utcnow)
    # updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


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
    links = relationship("Link", back_populates="profile")
    educations = relationship("Education", back_populates="profile")
    experiences = relationship("Experience", back_populates="profile")
    skills = relationship("Skill", back_populates="profile")

