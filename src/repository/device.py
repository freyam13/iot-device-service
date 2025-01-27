from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from src.repository.base import EntityModel, Base


class DeviceRepo(EntityModel, Base):
    __tablename__ = "device"

    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    state = Column(String, nullable=True)
    paired_hub_id = Column(String, ForeignKey("hub.id"), nullable=True)

    paired_hub = relationship("HubRepo", back_populates="devices")
