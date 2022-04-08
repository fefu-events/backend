from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

from backend.database.base_class import Base


class Place(Base):
    id = Column(Integer, primary_key=True, index=True)
    label = Column(String(15), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    events = relationship("Event", back_populates="place")
