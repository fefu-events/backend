from sqlalchemy import Boolean, Column, Integer, String, and_,\
    select
from sqlalchemy.orm import relationship, object_session

from backend.database.base_class import Base
from backend.models.user_organization import UserOrganization


class Organization(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(250), nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    members = relationship(
        'User', lazy="select", secondary="userorganization",
        backref='Organization',
        viewonly=True)

    @property
    def owner_id(self):
        return object_session(self).\
            scalar(
                select(UserOrganization.user_id).
                where(
                    and_(
                        UserOrganization.organization_id == self.id,
                        UserOrganization.is_owner
                      )
                )
            )
