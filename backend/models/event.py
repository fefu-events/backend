from sqlalchemy import Column, ForeignKey, Integer, String,\
    select, func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship, object_session
from sqlalchemy_utc import UtcDateTime

from backend.database.base_class import Base
from backend.models.participation import Participation


class Event(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    description = Column(String(1000), nullable=False)
    date_begin = Column(UtcDateTime(), nullable=False)
    date_end = Column(UtcDateTime(), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id',
                                         ondelete="CASCADE"))
    user = relationship("User", back_populates="events")
    place_id = Column(Integer, ForeignKey('place.id',
                                          ondelete="CASCADE"))
    place = relationship("Place", back_populates="events")
    place_description = Column(String(100), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id',
                                             ondelete="CASCADE"))
    organization_id = Column(Integer, ForeignKey('organization.id',
                                                 ondelete="CASCADE"),
                             nullable=True)
    organization = relationship("Organization")
    category = relationship("Category")
    tags = Column(ARRAY(String(15)), server_default='{}')
    participations = relationship(
        "Participation",
        primaryjoin="Event.id == Participation.event_id")
    url = Column(String(2083), default=None, nullable=True)

    @property
    def participant_count(self):
        return object_session(self).\
            scalar(
                select(func.count(Participation.id)).
                where(Participation.event_id == self.id)
            )
