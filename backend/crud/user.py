from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from backend.crud.base import CRUDBase
from backend.models.user import User
from backend.models.user_subscription import UserSubscription
from backend.schemas.user import UserCreate, UserUpdate, UserUpdateAccess


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    def get_by_email(self, db: Session, email: str) -> User | None:
        return db.query(self.model). \
            filter(self.model.email == email).first()

    def get_multi_by_email_or_name(
        self, db: Session,
        search_query: str | None,
        skip: int = 0, limit: int = 100,
        moderator: bool | None = None,
    ) -> list[User]:
        query = db.query(User)

        if search_query:
            query = query.filter(or_(
                func.lower(User.name).contains(func.lower(search_query)),
                func.lower(User.email).contains(func.lower(search_query))
            ))

        if moderator:
            query = query.filter(User.is_moderator == True)

        return query. \
            order_by(User.id.desc()). \
            offset(skip). \
            limit(limit). \
            all()

    def get_followers(self, db: Session, user_id) -> list[User]:
        return db.query(User). \
            join(UserSubscription,
                 User.id == UserSubscription.follower_id). \
            filter(UserSubscription.user_id == user_id).all()

    def get_following(self, db: Session, user_id) -> list[User]:
        return db.query(User). \
            join(UserSubscription,
                 User.id == UserSubscription.user_id). \
            filter(UserSubscription.follower_id == user_id).all()

    def set_image(self, db: Session, user: User, image_uuid4: str):
        user.image_uuid4 = image_uuid4
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update_access(self, db: Session, user: User,
                      access_in: UserUpdateAccess) -> User:
        if access_in.is_moderator is not None:
            user.is_moderator = access_in.is_moderator
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def provide_admin_rights(self, db: Session, user: User) -> User:
        user.is_moderator = True
        user.is_admin = True
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def set_is_active(self, db: Session, user: User, is_active: bool) -> User:
        user.is_active = is_active
        db.add(user)
        db.commit()
        db.refresh(user)
        return user


user = CRUDUser(User)
