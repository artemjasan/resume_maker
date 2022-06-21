from sqlalchemy import (Column, Integer, String)
from sqlalchemy.orm import relationship

from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    profiles = relationship("Profile", back_populates="user", cascade="all, delete-orphan", lazy="selectin")
