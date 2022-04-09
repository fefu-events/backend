from sqlalchemy import Column, ForeignKey, Integer

from backend.database.base_class import Base


class Participation(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id',
                                         ondelete="CASCADE"))
    event_id = Column(Integer, ForeignKey('event.id',
                                          ondelete="CASCADE"))
