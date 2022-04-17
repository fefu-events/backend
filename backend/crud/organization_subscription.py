from sqlalchemy import and_
from sqlalchemy.orm import Session

from backend.crud.base import CRUDBase
from backend.models.organization_subscription import\
    OrganizationSubscription
from backend.schemas.organization_subscription import\
    OrganizationSubscriptionCreate


class CRUDOrganizationSubscription(
    CRUDBase[OrganizationSubscription,
             OrganizationSubscriptionCreate, None]
):

    def update():
        pass

    def get_by_users(self, db: Session, organization_id: int,
                     follower_id: int) -> OrganizationSubscription:
        return db.query(self.model).\
            filter(and_(self.model.organization_id == organization_id,
                        self.model.follower_id == follower_id)).\
            first()


organization_subscription = CRUDOrganizationSubscription(
    OrganizationSubscription)
