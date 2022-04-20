from fastapi import Depends, HTTPException, Request

from fastapi_azure_auth.user import User as UserAzureLib

from sqlalchemy.orm import Session

from backend import crud
from backend.api.dependencies.database import get_db
from backend.schemas.azure import (
    azure_scheme,
    azure_scheme_without_error
)
from backend.schemas.user import UserAzure
from backend.resources import strings


def get_user_azure(
    user_azure: UserAzureLib = Depends(azure_scheme)
) -> UserAzure:
    return UserAzure(
        email=user_azure.claims["preferred_username"],
        name=user_azure.claims["name"],
    )


def get_user_azure_without_error(
    user_azure: UserAzureLib = Depends(azure_scheme_without_error)
) -> UserAzure:
    if user_azure:
        return UserAzure(
            email=user_azure.claims["preferred_username"],
            name=user_azure.claims["name"],
        )
    return None


def user_exist(
    request: Request,
    user_azure: UserAzure = Depends(get_user_azure),
    db: Session = Depends(get_db),
):
    user = crud.user.get_by_email(db, user_azure.email)
    if not user:
        raise HTTPException(
            status_code=400,
            detail=strings.USER_DOES_NOT_EXIST_ERROR
        )
    request.state.current_user = user


def user_exist_without_error(
    request: Request,
    user_azure: UserAzure = Depends(get_user_azure_without_error),
    db: Session = Depends(get_db),
):
    user = None
    if user_azure:
        user = crud.user.get_by_email(db, user_azure.email)
    request.state.current_user = user
