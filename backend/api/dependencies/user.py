from typing import Callable

from fastapi import Depends, HTTPException, Request, Path, status

from fastapi_azure_auth.user import User as UserAzureLib

from sqlalchemy.orm import Session

from backend import crud
from backend.api.dependencies.database import get_db
from backend.schemas.azure import (
    azure_scheme,
    azure_scheme_without_error
)
from backend.schemas.user import UserAzure, UserInDBBase
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
) -> UserAzure | None:
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
            detail=strings.USER_DOES_NOT_EXIST
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


def _get_current_user(
    user_azure: UserAzure = Depends(get_user_azure),
    db: Session = Depends(get_db),
) -> UserInDBBase:
    if user_azure:
        user = crud.user.get_by_email(db, user_azure.email)
        if user:
            return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=strings.USER_DOES_NOT_EXIST
    )


def _get_current_user_optional(
    user_azure: UserAzure = Depends(get_user_azure_without_error),
    db: Session = Depends(get_db),
) -> UserInDBBase | None:
    if user_azure:
        return crud.user.get_by_email(db, user_azure.email)
    return None


def get_current_user(
    *,
    required: bool = True
) -> Callable:
    return _get_current_user if required else _get_current_user_optional


def get_user_by_id_from_path(
    user_id: int = Path(..., ge=1),
    db=Depends(get_db)
) -> UserInDBBase:
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strings.USER_DOES_NOT_EXIST
        )
    return user
