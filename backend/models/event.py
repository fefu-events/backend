from sqlalchemy import (
    ARRAY, Column, DateTime, Integer, String, ForeignKey
)
from sqlalchemy.orm import relationship

from backend.database.base_class import Base


class Event(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    description = Column(
        String(1000), nullable=False)
    date_begin = Column(DateTime, nullable=False)
    date_end = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="events")
    place_description = Column(
        String(100), nullable=False)
    tags = Column(ARRAY(String(15)), server_default='{}')
