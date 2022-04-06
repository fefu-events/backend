from typing import Any, Optional

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


event = CRUDEvent(Event)
