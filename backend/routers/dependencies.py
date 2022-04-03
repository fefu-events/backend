from backend.models.user import UserBase
from fastapi import Request, Depends, HTTPException

from fastapi_azure_auth.user import User as UserAzure
from sqlmodel import Session, select

from backend.database import engine
from backend.models.user import User
from backend.routers.authentication import azure_scheme


def get_user_info_from_schema(user: UserAzure):
    user_process = {
        "email": user.claims["preferred_username"],
        "name": user.claims["name"]
    }
    return UserBase(**user_process)


def user_exist(request: Request,
               user_azure: UserAzure = Depends(azure_scheme)):
    user_azure_parsed = get_user_info_from_schema(user_azure)
    with Session(engine) as session:
        user: User | None = session.exec(
            select(User).where(User.email == user_azure_parsed.email)
        ).first()
        if not user:
            raise HTTPException(
                status_code=400,
                detail="The user is not exist"
            )
        request.state.current_user = user
