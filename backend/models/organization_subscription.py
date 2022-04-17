from sqlalchemy import Column, ForeignKey, Integer

from backend.database.base_class import Base


class OrganizationSubscription(Base):
    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey('user.id',
                                             ondelete="CASCADE"))
    organization_id = Column(Integer, ForeignKey('organization.id',
                                                 ondelete="CASCADE"))
