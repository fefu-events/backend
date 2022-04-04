from typing import Generator
from fastapi import Request, Depends, HTTPException

from sqlalchemy.orm import Session

from fastapi_azure_auth.user import User as UserAzure

from backend.schemas.user import UserBase
from backend.routers.authentication import azure_scheme
from backend.resources import strings
from backend.database.session import SessionLocal
from backend import crud


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_user_azure(
    user_azure: UserAzure = Depends(azure_scheme)
) -> UserBase:
    return UserBase(
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
