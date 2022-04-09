from sqlalchemy import Column, Integer, ForeignKey

from backend.database.base_class import Base


class UserSubscription(Base):
    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey('user.id',
                                             ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey('user.id',
                                         ondelete="CASCADE"))
