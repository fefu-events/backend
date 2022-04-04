from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(BaseModel):
    pass


class UserUpdate(BaseModel):
    pass

