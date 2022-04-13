from sqlalchemy import and_
from sqlalchemy.orm import Session

from backend.crud.base import CRUDBase
from backend.models.participation import Participation
from backend.schemas.participation import ParticipationCreate,\
    ParticipationInDBBase


class CRUDParticipation(
    CRUDBase[Participation, ParticipationCreate, None]
):

    def get_by_event_and_user(
        self, db: Session, event_id: int, user_id: int
    ) -> Participation | None:
        return db.query(Participation).\
            filter(and_(Participation.event_id == event_id,
                        Participation.user_id == user_id)).first()

    def create_with_user(
        self, db: Session, *, event_id: int, user_id: int
    ) -> Participation:
        db_obj = Participation(event_id=event_id, user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


participation = CRUDParticipation(Participation)
