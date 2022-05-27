from fastapi import APIRouter, Depends, HTTPException, status

from backend import crud
from backend.api.dependencies.database import get_db
from backend.api.dependencies.user import (
    get_user_by_id_from_path,
    get_current_user
)
from backend.resources import strings
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
    search_query: str | None = None,
    moderator: bool | None = None,
    current_user: UserInDBBase = Depends(get_current_user(required=False)),
    db=Depends(get_db),
):
    if moderator:
        if current_user is None or not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=strings.DONT_HAVE_ACCESS
            )

    return crud.user.get_multi_by_email_or_name(
        db, skip=skip, limit=limit, search_query=search_query,
        moderator=moderator)


@router.get(
    '/{user_id}/',
    name="user:get_by_id",
    response_model=UserWithOrganizationsInDBBase,
)
def get_user(
    user: UserInDBBase = Depends(get_user_by_id_from_path),
    current_user: UserInDBBase =
    Depends(get_current_user(required=False)),
    db=Depends(get_db),
):
    if current_user:
        user.am_i_following = crud.user_subscription. \
                                  get_by_users(db, user_id=user.id,
                                               follower_id=current_user.id) is not None
    return user
