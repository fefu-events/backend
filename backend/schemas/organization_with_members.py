from backend.schemas.user import UserInDBBase
from backend.schemas.organization import OrganizationInDBBase


class OrganizationInDBBaseWithMembers(OrganizationInDBBase):
    members: list[UserInDBBase] | None
