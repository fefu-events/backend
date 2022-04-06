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


@router.put(
    "/me/update",
    name="user:update",
    response_model=UserInDBBase,
    dependencies=[Depends(user_exist)],
)
def update_me(
    request: Request,
    user_in: UserUpdate,
    db=Depends(get_db),
):
    request.state.current_user =\
        crud.user.update(db,
                         db_obj=request.state.current_user,
                         obj_in=user_in)
    return request.state.current_user


@router.post(
    "/register",
    name="user:register",
    response_model=UserAzure,
)
async def register(
    user_azure: UserAzure = Depends(get_user_azure),
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
