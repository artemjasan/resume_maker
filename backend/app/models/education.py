from sqlalchemy import (Column, ForeignKey, Integer, String, Date, UniqueConstraint)
from sqlalchemy.orm import relationship

from app.database.database import Base


class Education(Base):
    __tablename__ = "educations"
    __table_args__ = (
        UniqueConstraint('name', 'profile_id', name='unique_name_profile'),
    )
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    specialization = Column(String(256), nullable=False)
    description = Column(String(512), nullable=False)
    since = Column(Date, nullable=False)
    until = Column(Date, nullable=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    profile = relationship("Profile", back_populates="educations")
