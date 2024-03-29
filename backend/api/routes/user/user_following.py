from fastapi import APIRouter, Depends, HTTPException, status

from backend import crud
from backend.api.dependencies.database import get_db
from backend.api.dependencies.user import (
    user_exist,
    get_current_user,
    get_user_by_id_from_path
)
from backend.resources import strings
from backend.schemas.message import Message
from backend.schemas.subscription import Subscription
from backend.schemas.user import UserInDBBase
from backend.schemas.user_subscription import (
    UserSubscriptionCreate,
    UserSubscriptionInDBBase,
)

router = APIRouter(
    tags=["user following"],
)


@router.post(
    '/{user_id}/follow/',
    name="user:follow_by_id",
    response_model=UserSubscriptionInDBBase,
    dependencies=[Depends(user_exist)],
)
def follow_user(
    current_user: UserInDBBase = Depends(get_current_user()),
    user: UserInDBBase = Depends(get_user_by_id_from_path),
    db=Depends(get_db),
):
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=strings.UNABLE_TO_FOLLOW_YOURSELF,
        )
    create_data = {
        'user_id': user.id,
        'follower_id': current_user.id
    }
    user_subscription = crud.user_subscription.get_by_users(
        db, **create_data)
    if user_subscription:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=strings.USER_IS_ALREADY_FOLLOWED
        )
    return crud.user_subscription.create(
        db, obj_in=UserSubscriptionCreate(**create_data))


@router.delete(
    '/{user_id}/unfollow/',
    name="user:unfollow_by_id",
    response_model=Message,
)
def unfollow_user(
    current_user: UserInDBBase = Depends(get_current_user()),
    user: UserInDBBase = Depends(get_user_by_id_from_path),
    db=Depends(get_db),
):
    user_subscription = crud.user_subscription.get_by_users(
        db, user_id=user.id, follower_id=current_user.id,
    )
    if not user_subscription:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=strings.USER_IS_NOT_FOLLOWED
        )
    crud.user_subscription.remove(db, id=user_subscription.id)  # type: ignore
    return Message(detail=strings.USER_IS_NOT_FOLLOWED)


@router.get(
    '/{user_id}/followers/',
    name="user:get_followers_by_user_id",
    response_model=list[UserInDBBase],
)
def get_followers(
    user_id: int,
    db=Depends(get_db),
):
    return crud.user.get_followers(db, user_id=user_id)


@router.get(
    '/{user_id}/following/',
    name="user:get_followers_by_user_id",
    response_model=list[Subscription],
)
def get_following(
    user_id: int,
    db=Depends(get_db),
):
    return crud.user.get_following(db, user_id=user_id)
