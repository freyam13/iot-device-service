from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from src.repository.base import EntityModel, Base


class DwellingRepo(EntityModel, Base):
    __tablename__ = "dwelling"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    is_occupied = Column(Boolean, default=False, nullable=False)

    hubs = relationship("HubRepo", back_populates="dwelling")
