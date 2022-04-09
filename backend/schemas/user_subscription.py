from pydantic import BaseModel


class UserSubscriptionBase(BaseModel):
    pass


class UserSubscriptionCreate(UserSubscriptionBase):
    user_id: int
    follower_id: int


class UserSubscriptionInDBBase(UserSubscriptionBase):
    user_id: int
    follower_id: int

    class Config:
        orm_mode = True
