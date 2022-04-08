from pydantic import BaseModel, EmailStr


class UserAzure(BaseModel):
    name: str
    email: str


class UserBase(BaseModel):
    name: str
    email: str
    is_admin: bool
    is_moderator: bool
    tags: list[str]


class UserCreate(BaseModel):
    pass


class UserUpdate(BaseModel):
    tags: list[str]


class UserInDBBase(UserBase):
    id: int

    class Config:
        orm_mode = True
