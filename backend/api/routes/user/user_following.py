from fastapi import APIRouter, Depends, HTTPException, Request

from backend import crud
from backend.api.dependencies.database import get_db
from backend.api.dependencies.user import (
    user_exist,
    get_current_user,
    get_user_by_id_from_path
)
from backend.schemas.user import UserInDBBase
from backend.schemas.user_subscription import (
    UserSubscriptionCreate,
    UserSubscriptionInDBBase,
)
from backend.schemas.message import Message
from backend.resources import strings

router = APIRouter(
    tags=["user following"],
)


@router.post(
    '/{user_id}/follow',
    name="user:follow_by_id",
    response_model=UserSubscriptionInDBBase,
    dependencies=[Depends(user_exist)],
)
def follow_user(
    request: Request,
    current_user: UserInDBBase = Depends(get_current_user()),
    user: UserInDBBase = Depends(get_user_by_id_from_path),
    db=Depends(get_db),
):
    if user.id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail=strings.CAN_NOT_SUBSCRIBE_TO_YOURSELF,
        )
    create_data = {
        'user_id': user.id,
        'follower_id': current_user.id
    }
    user_subscription = crud.user_subscription.get_by_users(
        db, **create_data)
    if user_subscription:
        raise HTTPException(
            status_code=409,
            detail=strings.HAVE_ALREADY_SUBSCRIBED_TO_THIS_USER_ERROR,
        )
    return crud.user_subscription.create(
        db, obj_in=UserSubscriptionCreate(**create_data))


@router.delete(
    '/{user_id}/unfollow',
    name="user:unfollow_by_id",
    response_model=Message,
    dependencies=[Depends(user_exist)],
)
def unfollow_user(
    user_id: int,
    current_user: UserInDBBase = Depends(get_current_user()),
    user: UserInDBBase = Depends(get_user_by_id_from_path),
    db=Depends(get_db),
):
    user_subscription = crud.user_subscription.get_by_users(
        db, user_id=user.id, follower_id=current_user.id,
    )
    if not user_subscription:
        raise HTTPException(
            status_code=409,
            detail=strings.ARE_NOT_FOLLOWING_THIS_USER,
        )
    crud.user_subscription.remove(db, id=user_subscription.id)
    return Message(detail=strings.ARE_NOT_FOLLOWING_THIS_USER)


@router.get(
    '/{user_id}/followers',
    name="user:get_followers_by_user_id",
    response_model=list[UserInDBBase],
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
)
def get_following(
    request: Request,
    user_id: int,
    db=Depends(get_db),
):
    return crud.user.get_following(db, user_id=user_id)
