from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from backend.database.base_class import Base


class Event(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    description = Column(String(1000), nullable=False)
    date_begin = Column(DateTime, nullable=False)
    date_end = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id',
                                         ondelete="CASCADE"))
    user = relationship("User", back_populates="events")
    place_id = Column(Integer, ForeignKey('place.id',
                                          ondelete="CASCADE"))
    place = relationship("Place", back_populates="events")
    place_description = Column(String(100), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id',
                                             ondelete="CASCADE"))
    category = relationship("Category", back_populates="events")
    tags = Column(ARRAY(String(15)), server_default='{}')
    participations = relationship(
        "Participation",
        primaryjoin="Event.id == Participation.event_id")
