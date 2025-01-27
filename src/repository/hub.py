from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from src.repository.base import EntityModel, Base


class HubRepo(EntityModel, Base):
    __tablename__ = "hub"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    dwelling_id = Column(String, ForeignKey("dwelling.id"), nullable=True)

    devices = relationship("DeviceRepo", back_populates="paired_hub")
