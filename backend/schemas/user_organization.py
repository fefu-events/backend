from pydantic import BaseModel, Field


class UserOrganizationBase(BaseModel):
    pass


class UserOrganizationCreate(UserOrganizationBase):
    user_id: int
    organization_id: int


class UserOrganizationUpdate(BaseModel):
    is_owner: bool


class UserOrganizationDelete(BaseModel):
    user_id: int


class UserOrganizationCreateWithIsOwner(UserOrganizationCreate):
    is_owner: bool = Field(default=False)


class UserOrganizationInDBBase(UserOrganizationBase):
    is_owner: bool = Field(default=False)

    class Config:
        orm_mode = True
