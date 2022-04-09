from fastapi import APIRouter, Depends, Request

from backend import crud
from backend.routers.dependencies import get_db, get_user_azure
from backend.schemas.user import CurrentUserExist, UserAzure

router = APIRouter(
    prefix="/current-user-exist",
    tags=["current-user-exist"],
)


@router.get(
    "/",
    name="current-user-exist:get",
    response_model=CurrentUserExist,
)
def get_me(
    request: Request,
    user_azure: UserAzure = Depends(get_user_azure),
    db=Depends(get_db),
):
    user_exist =\
        crud.user.get_by_email(db, user_azure.email) is not None
    return CurrentUserExist(exist=user_exist)
