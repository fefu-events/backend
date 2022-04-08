from pydantic import BaseModel, constr


class CategoryBase(BaseModel):
    label: constr(max_length=100)


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryCreate):
    pass


class CategoryInDBBase(CategoryBase):
    id: int

    class Config:
        orm_mode = True
