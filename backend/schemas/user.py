from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(BaseModel):
    pass


class UserUpdate(BaseModel):
    pass


class UserInDBBase(UserBase):
    id: int

    class Config:
        orm_mode = True

