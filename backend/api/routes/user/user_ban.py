from fastapi import APIRouter, Depends, HTTPException, status

from backend import crud
from backend.api.dependencies.database import get_db
from backend.api.dependencies.user import (
    user_exist,
    get_current_user,
    get_user_by_id_from_path
)
from backend.schemas.user import UserInDBBase

router = APIRouter()


@router.post(
    '/{user_id}/ban/',
    name="user:ban",
    response_model=UserInDBBase,
    dependencies=[Depends(user_exist)],
)
def ban_user(
    current_user: UserInDBBase = Depends(get_current_user()),
    user: UserInDBBase = Depends(get_user_by_id_from_path),
    db=Depends(get_db),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )
    return crud.user.set_is_active(db, user, False)


@router.post(
    '/{user_id}/unban/',
    name="user:unban",
    response_model=UserInDBBase,
    dependencies=[Depends(user_exist)],
)
def unban_user(
    current_user: UserInDBBase = Depends(get_current_user()),
    user: UserInDBBase = Depends(get_user_by_id_from_path),
    db=Depends(get_db),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )
    return crud.user.set_is_active(db, user, True)
