from pydantic import BaseModel, EmailStr

from backend.schemas.organization import OrganizationInDBBase


class CurrentUserExist(BaseModel):
    exist: bool


class UserAzure(BaseModel):
    name: str
    email: str

    def get_test_headers(self) -> dict[str, str]:
        return {
            "authoriozation": f"{self.name}:{self.email}"
        }


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
    image_uuid4: str | None

    class Config:
        orm_mode = True


class UserWithOrganizationsInDBBase(UserInDBBase):
    organizations: list[OrganizationInDBBase]
