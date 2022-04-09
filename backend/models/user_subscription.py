from typing import TYPE_CHECKING

from sqlalchemy import ARRAY, Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from backend.database.base_class import Base


class UserSubscription(Base):
    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey('user.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
