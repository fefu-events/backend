from sqlalchemy import and_
from sqlalchemy.orm import Session

from backend.crud.base import CRUDBase
from backend.crud.user_organization import user_organization as\
    crud_user_organization
from backend.models.organization import Organization
from backend.models.user_organization import UserOrganization
from backend.schemas.organization import OrganizationCreate,\
    OrganizationUpdate
from backend.schemas.user_organization import\
    UserOrganizationCreateWithIsOwner


class CRUDOrganization(
        CRUDBase[Organization, OrganizationCreate, OrganizationUpdate]
):

    def create_with_user(
        self, db: Session, *, obj_in: OrganizationCreate,
        user_id: int
    ) -> Organization:
        organization = self.create(db, obj_in=obj_in)
        crud_user_organization.create(
            db, obj_in=UserOrganizationCreateWithIsOwner(
                user_id=user_id,
                organization_id=organization.id,
                is_owner=True
            ))

        return organization

    def get_count_owners(
        self, db: Session, *, db_obj: Organization
    ) -> int:
        return db.query(UserOrganization).\
            filter(
                and_(
                    UserOrganization.organization_id == db_obj.id,
                    UserOrganization.is_owner
                )).\
            count()


organization = CRUDOrganization(Organization)
