from pydantic import BaseModel, constr


class OrganizationBase(BaseModel):
    title: constr(max_length=100)
    description: constr(max_length=250)


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationCreateWithMembers(OrganizationBase):
    members_ids: list[int]


class OrganizationUpdate(OrganizationCreate):
    pass


class OrganizationTransferOwnership(BaseModel):
    user_id: int


class OrganizationInDBBase(OrganizationBase):
    id: int
    is_verified: bool
    owner_id: int | None
    am_i_following: bool = False

    class Config:
        orm_mode = True
