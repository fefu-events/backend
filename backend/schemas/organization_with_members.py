from backend.schemas.user import UserInDBBase
from backend.schemas.organization import OrganizationInDBBase


class OrganizationInDBBaseWithMembers(OrganizationInDBBase):
    members: list[UserInDBBase] | None
    am_i_following: bool = False
