from typing import Generator

from fastapi import Depends, HTTPException, Request
from fastapi_azure_auth.user import User as UserAzureLib
from sqlalchemy.orm import Session

from backend import crud
from backend.database.session import SessionLocal
from backend.resources import strings
from backend.routers.authentication import azure_scheme
from backend.schemas.user import UserAzure


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_user_azure(
    user_azure: UserAzureLib = Depends(azure_scheme)
) -> UserAzure:
    return UserAzure(
        email=user_azure.claims["preferred_username"],
        name=user_azure.claims["name"],
    )


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
