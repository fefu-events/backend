from fastapi import APIRouter, Depends, HTTPException, Request

from backend import crud
from backend.api.dependencies.database import get_db
from backend.api.dependencies.user import get_user_azure, user_exist
from backend.schemas.user import (
    UserAzure,
    UserInDBBase,
    UserWithOrganizationsInDBBase,
    UserUpdate,
)
from backend.resources import strings

router = APIRouter()


@router.get(
    "/",
    name="me:get",
    response_model=UserWithOrganizationsInDBBase,
    dependencies=[Depends(user_exist)],
)
def get_me(
    request: Request,
    db=Depends(get_db),
):
    return request.state.current_user


@router.put(
    "/",
    name="me:update",
    response_model=UserInDBBase,
    dependencies=[Depends(user_exist)],
)
def update_me(
    request: Request,
    user_in: UserUpdate,
    db=Depends(get_db),
):
    request.state.current_user =\
        crud.user.update(
            db, db_obj=request.state.current_user, obj_in=user_in)
    return request.state.current_user


@router.post(
    "/",
    name="me:create",
    status_code=201,
    response_model=UserInDBBase,
)
async def register(
    user_azure: UserAzure = Depends(get_user_azure),
    db=Depends(get_db),
):
    user = crud.user.get_by_email(db, user_azure.email)
    if user:
        raise HTTPException(
            status_code=409,
            detail=strings.USER_WITH_THIS_EMAIL_ALREADY_EXIST_ERROR
        )
    return crud.user.create(db, obj_in=user_azure)
