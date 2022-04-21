from fastapi import APIRouter, Depends, HTTPException, Request

from backend import crud
from backend.api.dependencies.database import get_db
from backend.api.dependencies.user import get_current_user
from backend.api.dependencies.organization import (
    get_organization_by_id_from_path
)
from backend.schemas.organization_subscription import (
    OrganizationSubscriptionCreate,
    OrganizationSubscriptionInDBBase,
)
from backend.schemas.organization import OrganizationInDBBase
from backend.schemas.user import UserInDBBase
from backend.schemas.message import Message
from backend.resources import strings

router = APIRouter()


@router.post(
    '/{organization_id}/follow',
    name="organization:follow_by_id",
    response_model=OrganizationSubscriptionInDBBase,
    tags=["organization following"],
)
def follow_organization(
    request: Request,
    organization_id: int,
    db=Depends(get_db),
    current_user: UserInDBBase = Depends(get_current_user()),
    organization: OrganizationInDBBase =
        Depends(get_organization_by_id_from_path),
):
    create_data = {
        'follower_id': request.state.current_user.id,
        'organization_id': organization_id
    }
    organization_subscription = crud.organization_subscription.\
        get_by_users(db, **create_data)
    if organization_subscription:
        raise HTTPException(
            status_code=409,
            detail=strings.ORGANIZATION_IS_ALREADY_FOLLOWED
        )
    return crud.organization_subscription.create(
        db, obj_in=OrganizationSubscriptionCreate(**create_data))


@router.delete(
    '/{organization_id}/unfollow',
    name="organization:unfollow_by_id",
    response_model=Message,
    tags=["organization following"],
)
def unfollow_organization(
    request: Request,
    organization_id: int,
    db=Depends(get_db),
    current_user: UserInDBBase = Depends(get_current_user()),
    organization: OrganizationInDBBase =
        Depends(get_organization_by_id_from_path),
):
    data = {
        'follower_id': request.state.current_user.id,
        'organization_id': organization_id
    }
    organization_subscription = crud.organization_subscription.\
        get_by_users(db, **data)
    if not organization_subscription:
        raise HTTPException(
            status_code=409,
            detail=strings.ORGANIZATION_IS_NOT_FOLLOWED
        )
    crud.organization_subscription.remove(
        db, id=organization_subscription.id)

    return Message(detail=strings.ORGANIZATION_IS_NOT_FOLLOWED)
