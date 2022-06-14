from sqlalchemy import (Column, ForeignKey, Integer, String)
from sqlalchemy.orm import relationship

from .base import Base


class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    url = Column(String, nullable=False)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    profile = relationship("Profile", back_populates="links")
