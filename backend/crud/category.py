from sqlalchemy.orm import Session

from backend.crud.base import CRUDBase
from backend.models.category import Category
from backend.schemas.category import CategoryCreate, CategoryUpdate


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):

    def get_by_label(self, db: Session, label: str) -> Category | None:
        return db.query(self.model).\
            filter(self.model.label == label).first()


category = CRUDCategory(Category)
