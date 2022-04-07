from typing import Any, Optional, List
from datetime import datetime

from sqlalchemy.orm import Session

from backend.crud.base import CRUDBase
from backend.models.event import Event
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
        self, db, skip, limit, title=None,
        date_begin: datetime = None, date_end: datetime = None,
        user_id=None, tags: List[str] = None
    ) -> List[Event]:
        query = db.query(self.model)

        if title:
            query = query.filter(Event.title.contains(title))

        if date_begin:
            query = query.filter(Event.date_begin >= date_begin)

        if date_end:
            query = query.filter(Event.date_begin <= date_end)

        if user_id:
            query = query.filter(Event.user_id == user_id)

        if tags:
            query = query.filter(Event.tags.contains(tags))

        return query.\
            order_by(Event.date_begin.desc(), Event.id.desc()).\
            offset(skip).limit(limit).\
            all()


event = CRUDEvent(Event)
