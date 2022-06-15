from sqlalchemy import (Column, ForeignKey, Integer, String, UniqueConstraint)
from sqlalchemy.orm import relationship

from .base import Base


class Skill(Base):
    __tablename__ = "skills"
    __table_args__ = (
        UniqueConstraint('name', 'profile_id', name='unique_name_profile_skill'),
    )
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    proficiency = Column(Integer, nullable=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    profile = relationship("Profile", back_populates="skills")
