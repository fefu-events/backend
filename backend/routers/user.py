from fastapi import APIRouter, Depends, HTTPException, Request

from backend.resources import strings
from backend.schemas.user import (
    UserBase, UserInDBBase
)
from backend.routers.dependencies import (
    get_db, user_exist, get_user_azure
)
from backend import crud

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.get(
    '/all',
)
def get_usets(*, db=Depends(get_db)):
    return crud.user.get_multi(db)


@router.get(
    '/get/{user_id}',
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


@router.get(
    "/me",
    name="user:getme",
    description="Get current profile information",
    response_model=UserInDBBase,
    dependencies=[Depends(user_exist)],
)
def get_me(
    request: Request,
    db=Depends(get_db),
):
    return request.state.current_user


@router.get(
    "/register",
    name="user:register",
    response_model=UserBase,
)
async def register(
    user_azure: UserBase = Depends(get_user_azure),
    db=Depends(get_db),
):
    user = crud.user.get_by_email(db, user_azure.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail=strings.USER_WITH_THIS_EMAIL_ALREADY_EXIST_ERROR
        )
    crud.user.create(db, obj_in=user_azure)
    return user_azure
