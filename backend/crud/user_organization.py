from sqlalchemy import and_
from sqlalchemy.orm import Session

from backend.crud.base import CRUDBase
from backend.models.user_organization import UserOrganization
from backend.schemas.user_organization import UserOrganizationCreate


class CRUDUserOrganization(
        CRUDBase[UserOrganization, UserOrganizationCreate, None]
):
    def get_by_user_and_organization(
        self, db: Session, user_id: int, organization_id: int
    ) -> UserOrganization:
        return db.query(self.model).\
            filter(
                and_(
                    self.model.user_id == user_id,
                    self.model.organization_id == organization_id
                )).first()


user_organization = CRUDUserOrganization(UserOrganization)
