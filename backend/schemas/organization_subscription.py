from pydantic import BaseModel


class OrganizationSubscriptionBase(BaseModel):
    pass


class OrganizationSubscriptionCreate(OrganizationSubscriptionBase):
    follower_id: int
    organization_id: int


class OrganizationSubscriptionInDBBase(OrganizationSubscriptionBase):
    follower_id: int
    organization_id: int

    class Config:
        orm_mode = True
