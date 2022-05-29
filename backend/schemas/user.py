from pydantic import BaseModel
from pydantic.types import constr

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

    def get_test_headers(self) -> dict[str, str]:
        return {
            "authoriozation": f"{self.name}:{self.email}"
        }


class UserCreate(BaseModel):
    pass


class UserUpdate(BaseModel):
    tags: list[constr(max_length=30)]


class UserUpdateAccess(BaseModel):
    is_moderator: bool | None


class UserInDBBase(UserBase):
    id: int
    is_active: bool
    image_uuid4: str | None

    class Config:
        orm_mode = True


class UserWithOrganizationsInDBBase(UserInDBBase):
    organizations: list[OrganizationInDBBase]
    am_i_following: bool = False
