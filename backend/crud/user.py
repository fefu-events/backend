from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from backend.crud.base import CRUDBase
from backend.models.user import User
from backend.models.user_subscription import UserSubscription
from backend.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    def get_by_email(self, db: Session, email: any) -> User | None:
        return db.query(self.model).\
            filter(self.model.email == email).first()

    def get_multi_by_email_or_name(
        self, db: Session, search_query: str,
        skip: int = 0, limit: int = 100,
    ) -> list[User]:
        query = db.query(User)

        if search_query:
            query = query.filter(or_(
                func.lower(User.name).contains(func.lower(search_query)),
                func.lower(User.email).contains(func.lower(search_query))
            ))

        return query.\
            order_by(User.id.desc()).\
            offset(skip).\
            limit(limit).\
            all()


    def get_followers(self, db: Session, user_id) -> list[User]:
        return db.query(User).\
            join(UserSubscription,
                 User.id == UserSubscription.follower_id).\
            filter(UserSubscription.user_id == user_id).all()

    def get_following(self, db: Session, user_id) -> list[User]:
        return db.query(User).\
            join(UserSubscription,
                 User.id == UserSubscription.user_id).\
            filter(UserSubscription.follower_id == user_id).all()


user = CRUDUser(User)
