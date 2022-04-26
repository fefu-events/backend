from fastapi import APIRouter, Depends

from backend import crud
from backend.api.dependencies.database import get_db
from backend.api.dependencies.user import get_user_azure
from backend.schemas.user import CurrentUserExist, UserAzure

router = APIRouter()


@router.get(
    "/",
    name="current-user-exist:get",
    response_model=CurrentUserExist,
)
def get_me(
    user_azure: UserAzure = Depends(get_user_azure),
    db=Depends(get_db),
):
    user_exist =\
        crud.user.get_by_email(db, user_azure.email) is not None
    return CurrentUserExist(exist=user_exist)
