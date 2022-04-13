from pydantic import BaseModel, constr


class OrganizationBase(BaseModel):
    title: constr(max_length=100)
    description: constr(max_length=250)
    tags: list[constr(max_length=15)]


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(OrganizationCreate):
    pass


class CategoryInDBBase(OrganizationBase):
    id: int

    class Config:
        orm_mode = True
