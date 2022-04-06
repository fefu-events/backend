from fastapi import APIRouter, Depends, HTTPException, Request

from backend import crud
from backend.resources import strings
from backend.routers.dependencies import get_db, get_user_azure, user_exist
from backend.schemas.user import UserAzure, UserUpdate, UserInDBBase

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.get(
    '/',
    name="user:get_all",
)
def get_users(
    skip: int = 0,
    limit: int = 100,
    db=Depends(get_db),
):
    return crud.user.get_multi(db, skip=skip, limit=limit)


@router.get(
    '/{user_id}',
    name="user:get",
    description="Get user by id",
    response_model=UserInDBBase,
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
