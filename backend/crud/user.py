from typing import Any, Optional

from sqlalchemy.orm import Session

from backend.crud.base import CRUDBase
from backend.models.user import User
from backend.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    def get_by_email(self, db: Session, email: Any) -> Optional[User]:
        return db.query(self.model).\
            filter(self.model.email == email).first()


user = CRUDUser(User)
