from sqlalchemy import ARRAY, Boolean, Column, Integer, String
from sqlalchemy.orm import relationship, backref

from backend.database.base_class import Base
from backend.models.user_organization import UserOrganization


class Organization(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(250), nullable=False)
    tags = Column(ARRAY(String(15)), server_default='{}')
    is_verified = Column(Boolean, default=False, nullable=False)
    members = relationship(
        'User', lazy="joined", secondary="userorganization",
        backref='Organization',
        viewonly=True)
