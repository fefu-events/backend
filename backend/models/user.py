from sqlalchemy import ARRAY, Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from backend.database.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True, index=True, nullable=False)
    tags = Column(ARRAY(String(15)), server_default='{}')
    is_admin = Column(Boolean, default=False, nullable=False)
    is_moderator = Column(Boolean, default=False, nullable=False)
    events = relationship("Event", back_populates="user")
    followers = relationship(
        "UserSubscription",
        primaryjoin="User.id == UserSubscription.user_id")
    following = relationship(
        "UserSubscription",
        primaryjoin="User.id == UserSubscription.follower_id")
    participations = relationship(
        "Participation",
        primaryjoin="User.id == Participation.user_id")
    organizations = relationship(
        'Organization', lazy="select", secondary="userorganization",
        backref='User',
        viewonly=True)
