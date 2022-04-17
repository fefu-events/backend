from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.crud.base import CRUDBase
from backend.models.category import Category
from backend.models.event import Event
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
        self, db, skip: int, limit: int = 100, title: str = None,
        date_begin: datetime = None, date_end: datetime = None,
        user_id: int = None, organization_id: int = None,
        category_id: int = None, place_id: int = None,
        tags: list[str] = None, user: User = None,
        subscriptions: bool = True, personalize_tags: bool = True,
    ) -> list[Event]:
        query = db.query(self.model).join(Place).join(Category)

        if user and subscriptions:
            query = query.join(
                UserSubscription,
                user.id == UserSubscription.follower_id)
            query = query.filter(
                Event.user_id == UserSubscription.user_id)

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

        if category_id:
            query = query.filter(
                Event.category_id == category_id)

        if place_id:
            query = query.filter(
                Event.place_id == place_id)

        if tags:
            query = query.filter(Event.tags.contains(tags))

        if user and personalize_tags:
            query = query.filter(Event.tags.overlap(user.tags))

        return query.\
            order_by(Event.date_begin.desc(), Event.id.desc()).\
            offset(skip).limit(limit).\
            all()


event = CRUDEvent(Event)
