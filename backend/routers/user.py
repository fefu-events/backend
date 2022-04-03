from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi_azure_auth.user import User as UserAzure
from sqlmodel import Session, select

from backend.database import engine, get_session
from backend.models.user import User, UserCreate
from backend.routers.dependencies import (
    user_exist, get_user_azure
)
from backend.resources import strings

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.get(
    '',
    name="user:get",
    description="Get user by id",
    response_model=User,
)
def get_user(
    user_id: int,
):
    with Session(engine) as session:
        user = session.get(User, user_id)
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
    response_model=User,
    dependencies=[Depends(user_exist)],
)
def get_me(
    request: Request,
):
    return request.state.current_user


@router.get(
    "/register",
    name="user:register",
    response_model=UserCreate,
)
async def register(
    user_azure: UserAzure = Depends(get_user_azure),
    session: Session = Depends(get_session),
):
    with Session(engine) as session:
        users = session.exec(
            select(User).where(User.email == user_azure.email)
        ).all()
        if users:
            raise HTTPException(
                status_code=400,
                detail=strings.USER_WITH_THIS_EMAIL_ALREADY_EXIST_ERROR
            )
        else:
            user = User(
                name=user_azure.name,
                email=user_azure.email
            )
            session.add(user)
            session.commit()
            return user_azure
