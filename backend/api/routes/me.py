from fastapi import APIRouter, Depends, HTTPException, status

from backend import crud
from backend.api.dependencies.database import get_db
from backend.api.dependencies.user import (
    get_user_azure,
    get_current_user,
)
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
)
def get_me(
    user: UserWithOrganizationsInDBBase = Depends(get_current_user()),
    db=Depends(get_db),
):
    return user


@router.put(
    "/",
    name="me:update",
    response_model=UserInDBBase,
)
def update_me(
    user_in: UserUpdate,
    user: UserWithOrganizationsInDBBase = Depends(get_current_user()),
    db=Depends(get_db),
):
    return crud.user.update(db, db_obj=user, obj_in=user_in)


@router.post(
    "/",
    name="me:create",
    status_code=status.HTTP_201_CREATED,
    response_model=UserInDBBase,
)
def create_me(
    user_azure: UserAzure = Depends(get_user_azure),
    db=Depends(get_db),
):
    user = crud.user.get_by_email(db, user_azure.email)
    if user:
        raise HTTPException(
            status_code=409,
            detail=strings.EMAIL_TAKEN
        )
    return crud.user.create(db, obj_in=user_azure)
