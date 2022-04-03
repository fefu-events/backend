from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi_azure_auth.user import User as UserAzure
from sqlmodel import Session, select

from backend.database import engine, get_session
from backend.models.user import User, UserCreate
from backend.routers.authentication import azure_scheme
from backend.routers.dependencies import (
    user_exist, get_user_info_from_schema
)

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get(
    "/me",
    name="user:getme",
    description="Get current profile information",
    response_model=User,
    dependencies=[Depends(user_exist)]
)
def get_me(request: Request):
    return request.state.current_user


@router.get(
    "/register",
    name="user:register",
    response_model=UserCreate
)
async def register(user_azure: UserAzure = Depends(azure_scheme),
                   session: Session = Depends(get_session)):
    with Session(engine) as session:
        user_azure_parsed = get_user_info_from_schema(user_azure)
        users = session.exec(
            select(User).where(User.email == user_azure_parsed.email)
        ).all()
        if users:
            raise HTTPException(
                status_code=400,
                detail="The user with this email already exists"
            )
        else:
            user = User(
                name=user_azure_parsed.name,
                email=user_azure_parsed.email
            )
            session.add(user)
            session.commit()
            return user_azure_parsed
