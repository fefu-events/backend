from sqlalchemy.orm import Session

from backend.crud.base import CRUDBase
from backend.crud.user_organization import user_organization as\
    crud_user_organization
from backend.models.organization import Organization
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


organization = CRUDOrganization(Organization)
