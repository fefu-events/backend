from pydantic import BaseModel

from backend.schemas.organization import OrganizationInDBBase
from backend.schemas.user import UserInDBBase


class Subscription(BaseModel):
    organization: OrganizationInDBBase | None
    user: UserInDBBase | None
