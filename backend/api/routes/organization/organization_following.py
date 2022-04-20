from fastapi import APIRouter, Depends, HTTPException, Request

from backend import crud
from backend.api.dependencies.database import get_db
from backend.api.dependencies.user import user_exist
from backend.schemas.organization_subscription import (
    OrganizationSubscriptionCreate,
    OrganizationSubscriptionInDBBase,
)
from backend.schemas.message import Message
from backend.resources import strings

router = APIRouter()


@router.post(
    '/{organization_id}/follow',
    name="organization:follow_by_id",
    response_model=OrganizationSubscriptionInDBBase,
    dependencies=[Depends(user_exist)],
    tags=["organization following"],
)
def follow_organization(
    request: Request,
    organization_id: int,
    db=Depends(get_db),
):
    organization = crud.organization.get(db, organization_id)
    if not organization:
        raise HTTPException(
            status_code=404,
            detail=strings.ORGANIZATION_DOES_NOT_FOUND_ERROR
        )
    create_data = {
        'follower_id': request.state.current_user.id,
        'organization_id': organization_id
    }
    organization_subscription = crud.organization_subscription.\
        get_by_users(db, **create_data)
    if organization_subscription:
        raise HTTPException(
            status_code=409,
            detail=strings.HAVE_ALREADY_SUBSCRIBED_TO_THIS_ORGANIZATION_ERROR
        )
    return crud.organization_subscription.create(
        db, obj_in=OrganizationSubscriptionCreate(**create_data))


@router.delete(
    '/{organization_id}/unfollow',
    name="organization:unfollow_by_id",
    response_model=Message,
    dependencies=[Depends(user_exist)],
    tags=["organization following"],
)
def unfollow_organization(
    request: Request,
    organization_id: int,
    db=Depends(get_db),
):
    organization = crud.organization.get(db, organization_id)
    if not organization:
        raise HTTPException(
            status_code=404,
            detail=strings.ORGANIZATION_DOES_NOT_FOUND_ERROR
        )
    data = {
        'follower_id': request.state.current_user.id,
        'organization_id': organization_id
    }
    organization_subscription = crud.organization_subscription.\
        get_by_users(db, **data)
    if not organization_subscription:
        raise HTTPException(
            status_code=409,
            detail=strings.ARE_NOT_FOLLOWING_THIS_ORGANIZATION
        )
    crud.organization_subscription.remove(
        db, id=organization_subscription.id)

    return Message(
        detail=strings.ARE_NOT_FOLLOWING_THIS_ORGANIZATION)
