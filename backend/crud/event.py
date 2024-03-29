from datetime import datetime, timezone

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from backend.crud.base import CRUDBase
from backend.models.category import Category
from backend.models.event import Event
from backend.models.organization_subscription import \
    OrganizationSubscription
from backend.models.place import Place
from backend.models.user import User
from backend.models.user_subscription import UserSubscription
from backend.schemas.event import EventCreate, EventUpdate


class CRUDEvent(CRUDBase[Event, EventCreate, EventUpdate]):

    def create_with_user(
        self, db: Session, *, obj_in: EventCreate, user_id: int
    ):
        db_obj = self.model(**dict(obj_in), user_id=user_id)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_with_filter(
        self, db, skip: int, limit: int = 100,
        title: str | None = None,
        date_begin: datetime | None = None,
        date_end: datetime | None = None,
        user_id: int | None = None,
        organization_id: int | None = None,
        category_ids: list[int] | None = None,
        place_ids: list[int] | None = None,
        tags: list[str] | None = None,
        user: User | None = None,
        subscriptions: bool = True,
        personalize_tags: bool = True,
        archived: bool = False
    ) -> list[Event]:
        query = db.query(self.model).join(Place).join(Category)

        if user and subscriptions:  # noqa
            query = query.join(
                UserSubscription,
                user.id == UserSubscription.follower_id,
                isouter=True
            ).join(
                OrganizationSubscription,
                user.id == OrganizationSubscription.follower_id,
                isouter=True
            )
            query = query.filter(or_(
                Event.user_id == UserSubscription.user_id,
                Event.organization_id ==
                OrganizationSubscription.organization_id
            ))

        if title:
            query = query.filter(
                func.lower(Event.title).contains(func.lower(title)))

        if date_begin:
            query = query.filter(Event.date_begin >= date_begin)

        if date_end:
            query = query.filter(Event.date_end <= date_end)

        if user_id:
            query = query.filter(Event.user_id == user_id)

        if organization_id:
            query = query.filter(
                Event.organization_id == organization_id)

        if category_ids:
            query = query.filter(
                Event.category_id.in_(category_ids))

        if place_ids:
            query = query.filter(
                Event.place_id.in_(place_ids))

        if tags:
            query = query.filter(Event.tags.contains(tags))  # type: ignore

        if user and personalize_tags:
            query = query.filter(Event.tags.overlap(user.tags))

        if not archived:
            now = datetime.now(tz=timezone.utc)
            query = query.filter(Event.date_end > now)

        return query. \
            order_by(Event.date_begin.asc(), Event.id.desc()). \
            offset(skip).limit(limit). \
            all()


event = CRUDEvent(Event)
