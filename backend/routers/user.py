from fastapi import APIRouter, Depends, HTTPException, Request

from backend import crud
from backend.resources import strings
from backend.routers.dependencies import get_db, user_exist
from backend.schemas.user import UserInDBBase,\
    UserWithOrganizationsInDBBase
from backend.schemas.user_subscription import (UserSubscriptionCreate,
                                               UserSubscriptionInDBBase)
from backend.schemas.message import Message

router = APIRouter(
    prefix="/user",
)


@router.get(
    '/',
    name="user:get",
    response_model=list[UserInDBBase],
    tags=["user"],
)
def get_users(
    skip: int = 0,
    limit: int = 100,
    search_query: str = None,
    db=Depends(get_db),
):
    return crud.user.get_multi_by_email_or_name(
        db, skip=skip, limit=limit, search_query=search_query)


@router.get(
    '/{user_id}',
    name="user:get_by_id",
    response_model=UserWithOrganizationsInDBBase,
    tags=["user"],
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


@router.post(
    '/{user_id}/follow',
    name="user:follow_by_id",
    response_model=UserSubscriptionInDBBase,
    dependencies=[Depends(user_exist)],
    tags=["user following"],
)
def follow_user(
    request: Request,
    user_id: int,
    db=Depends(get_db),
):
    if user_id == request.state.current_user.id:
        raise HTTPException(
            status_code=400,
            detail=strings.CAN_NOT_SUBSCRIBE_TO_YOURSELF
        )
    user = crud.user.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=strings.USER_DOES_NOT_FOUND_ERROR
        )
    create_data = {
        'user_id': user_id,
        'follower_id': request.state.current_user.id
    }
    user_subscription = crud.user_subscription.get_by_users(
        db, **create_data)
    if user_subscription:
        raise HTTPException(
            status_code=409,
            detail=strings.HAVE_ALREADY_SUBSCRIBED_TO_THIS_USER_ERROR
        )
    return crud.user_subscription.create(
        db, obj_in=UserSubscriptionCreate(**create_data))


@router.delete(
    '/{user_id}/unfollow',
    name="user:unfollow_by_id",
    response_model=Message,
    dependencies=[Depends(user_exist)],
    tags=["user following"],
)
def unfollow_user(
    request: Request,
    user_id: int,
    db=Depends(get_db),
):
    user_subscription = crud.user_subscription.get_by_users(
        db, user_id=user_id,
        follower_id=request.state.current_user.id)
    if not user_subscription:
        raise HTTPException(
            status_code=409,
            detail=strings.ARE_NOT_FOLLOWING_THIS_USER
        )
    crud.user_subscription.remove(db, id=user_subscription.id)

    return Message(detail=strings.ARE_NOT_FOLLOWING_THIS_USER)


@router.get(
    '/{user_id}/followers',
    name="user:get_followers_by_user_id",
    response_model=list[UserInDBBase],
    tags=["user following"],
)
def get_followers(
    request: Request,
    user_id: int,
    db=Depends(get_db),
):
    return crud.user.get_followers(db, user_id=user_id)


@router.get(
    '/{user_id}/following',
    name="user:get_followers_by_user_id",
    response_model=list[UserInDBBase],
    tags=["user following"],
)
def get_following(
    request: Request,
    user_id: int,
    db=Depends(get_db),
):
    return crud.user.get_following(db, user_id=user_id)
