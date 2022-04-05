from typing import List

from pydantic import BaseModel, EmailStr


class UserAzure(BaseModel):
    name: str
    email: str


class UserBase(BaseModel):
    name: str
    email: str
    is_admin: bool
    is_moderator: bool
    tags: List[str]


class UserCreate(BaseModel):
    pass


class UserUpdate(BaseModel):
    pass


class UserInDBBase(UserBase):
    id: int

    class Config:
        orm_mode = True
