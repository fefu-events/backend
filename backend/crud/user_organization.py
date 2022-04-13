from backend.crud.base import CRUDBase
from backend.models.user_organization import UserOrganization
from backend.schemas.user_organization import UserOrganizationCreate


class CRUDUserOrganization(
        CRUDBase[UserOrganization, UserOrganizationCreate, None]
):
    pass


user_organization = CRUDUserOrganization(UserOrganization)
