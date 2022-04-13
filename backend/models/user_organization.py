from sqlalchemy import Boolean, Column, ForeignKey, Integer,\
    UniqueConstraint

from backend.database.base_class import Base


class UserOrganization(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id",
                                         ondelete="CASCADE"))
    organization_id = Column(Integer, ForeignKey("organization.id",
                                                 ondelete="CASCADE"))
    is_owner = Column(Boolean, default=False, nullable=False)

    __table_args__ = (
        UniqueConstraint("organization_id", "user_id",
                         name="unique_user_organization"),
    )
