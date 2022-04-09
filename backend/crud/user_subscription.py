from sqlalchemy import and_
from sqlalchemy.orm import Session

from backend.crud.base import CRUDBase
from backend.models.user_subscription import UserSubscription
from backend.schemas.user_subscription import\
    UserSubscriptionCreate


class CRUDEvent(
    CRUDBase[UserSubscription, UserSubscriptionCreate, None]
):

    def update():
        pass

    def get_by_users(self, db: Session, user_id: int,
                     follower_id: int) -> UserSubscription:
        return db.query(self.model).\
            filter(and_(self.model.user_id == user_id,
                        self.model.follower_id == follower_id)).\
            first()

user_subscription = CRUDEvent(UserSubscription)
