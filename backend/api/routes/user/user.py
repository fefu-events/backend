from fastapi import APIRouter, Depends, HTTPException

from backend import crud
from backend.api.dependencies.database import get_db
from backend.schemas.user import (
    UserInDBBase,
    UserWithOrganizationsInDBBase
)
from backend.resources import strings

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
    user_id: int,
    db=Depends(get_db),
):
    user = crud.user.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=strings.USER_DOES_NOT_FOUND_ERROR
        )
    return user
