from sqlalchemy.orm import Session

from backend.crud.base import CRUDBase
from backend.models.place import Place
from backend.schemas.place import PlaceCreate, PlaceUpdate


class CRUDUser(CRUDBase[Place, PlaceCreate, PlaceUpdate]):

    def get_by_label(self, db: Session, label: str) -> Place | None:
        return db.query(self.model).\
            filter(self.model.label == label).first()


place = CRUDUser(Place)
