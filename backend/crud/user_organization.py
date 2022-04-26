from sqlalchemy import and_
from sqlalchemy.orm import Session

from backend.crud.base import CRUDBase
from backend.models.user_organization import UserOrganization
from backend.schemas.user_organization import UserOrganizationCreate,\
    UserOrganizationUpdate


class CRUDUserOrganization(
        CRUDBase[UserOrganization, UserOrganizationCreate,
                 UserOrganizationUpdate]
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

    def transfer_owner(
        self, db: Session,
        user_organization_1: UserOrganization,
        user_organization_2: UserOrganization
    ) -> (UserOrganization, UserOrganization): # type: ignore
        user_organization_1.is_owner = False # type: ignore
        user_organization_2.is_owner = True # type: ignore
        db.add(user_organization_1)
        db.add(user_organization_2)
        db.commit()
        db.refresh(user_organization_1)
        db.refresh(user_organization_2)
        return (user_organization_1, user_organization_2)


user_organization = CRUDUserOrganization(UserOrganization)
