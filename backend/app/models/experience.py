from sqlalchemy import (Column, ForeignKey, Integer, String, Date, UniqueConstraint)
from sqlalchemy.orm import relationship

from .base import Base


class Experience(Base):
    __tablename__ = "experiences"
    __table_args__ = (
        UniqueConstraint('employer', 'position', 'profile_id', name='unique_position_employer_profile'),
    )
    id = Column(Integer, primary_key=True)
    employer = Column(String(128), nullable=False)
    position = Column(String(128), nullable=False)
    description = Column(String(512), nullable=False)
    since = Column(Date, nullable=False)
    until = Column(Date, nullable=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    profile = relationship("Profile", back_populates="experiences")
