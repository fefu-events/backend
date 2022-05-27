from datetime import datetime, timezone

from sqlalchemy import func, or_
from sqlalchemy.orm import Session, with_expression

from backend.crud.base import CRUDBase
from backend.models.category import Category
from backend.models.event import Event
from backend.models.organization_subscription import \
    OrganizationSubscription
from backend.models.place import Place
from backend.models.user import User
from backend.models.user_subscription import UserSubscription
from backend.schemas.place import PlaceCreate, PlaceUpdate


class CRUDUser(CRUDBase[Place, PlaceCreate, PlaceUpdate]):

    def get_by_label(self, db: Session, label: str) -> Place | None:
        return db.query(self.model). \
            filter(self.model.label == label).first()

    def get_for_map(
        self, db: Session,
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
        archived: bool = False,
    ) -> list[Place]:
        query = db.query(
            Place
        ).join(
            Event
        ).options(
            with_expression(
                Place.event_count,
                func.count(Event.id)
            )
        ).join(Category)

        if user and subscriptions:
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

        query = query.group_by(
            Place.id
        )
        return query.all()


place = CRUDUser(Place)
