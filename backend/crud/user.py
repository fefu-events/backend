from sqlalchemy import func, or_, and_
from sqlalchemy.orm import Session

from backend.crud.base import CRUDBase
from backend.models.organization import Organization
from backend.models.organization_subscription import OrganizationSubscription
from backend.models.user import User
from backend.models.user_subscription import UserSubscription
from backend.schemas.subscription import Subscription
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

    def get_following(self, db: Session, user_id) -> list[Subscription]:
        users = db.query(User).join(
            UserSubscription, User.id == UserSubscription.user_id). \
            filter(UserSubscription.follower_id == user_id).all()
        organizations = db.query(Organization). \
            join(OrganizationSubscription, and_(Organization.id == OrganizationSubscription.organization_id,
                                                OrganizationSubscription.follower_id == user_id)
                 ).all()
        result = []
        for item in organizations:
            result.append(Subscription(organization=item, user=None))
        for item in users:
            result.append(Subscription(organization=None, user=item))
        return result

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

"""
SELECT organization.id AS organization_id,
        organization.title AS organization_title,
        organization.description AS organization_description,
        organization.is_verified AS organization_is_verified 
FROM organization 
JOIN organizationsubscription ON "user".id = organizationsubscription.follower_id 
WHERE organizationsubscription.follower_id = %(follower_id_1)s

SELECT organization.id AS organization_id, organization.title AS organization_title, organization.description AS organization_description, organization.is_verified AS organization_is_verified 
FROM organization
JOIN "user"
    ON "user".id = %(id_1)s
JOIN organizationsubscription
    ON organizationsubscription.follower_id = %(follower_id_1)s
"""
