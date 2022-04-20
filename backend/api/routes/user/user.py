from fastapi import APIRouter, Depends

from backend import crud
from backend.api.dependencies.database import get_db
from backend.api.dependencies.user import (
    get_user_by_id_from_path
)
from backend.schemas.user import (
    UserInDBBase,
    UserWithOrganizationsInDBBase
)

router = APIRouter()


@router.get(
    '/',
    name="user:get",
    response_model=list[UserInDBBase],
)
def get_users(
    skip: int = 0,
    limit: int = 100,
    search_query: str = None,
    db=Depends(get_db),
):
    return crud.user.get_multi_by_email_or_name(
        db, skip=skip, limit=limit, search_query=search_query)


@router.get(
    '/{user_id}',
    name="user:get_by_id",
    response_model=UserWithOrganizationsInDBBase,
)
def get_user(
    user: UserInDBBase = Depends(get_user_by_id_from_path),
    db=Depends(get_db),
):
    return user
