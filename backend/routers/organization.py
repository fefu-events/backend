from fastapi import APIRouter, Depends, HTTPException, Request

from backend.resources import strings
from backend import crud
from backend.routers.dependencies import get_db, user_exist
from backend.schemas.organization import OrganizationCreate,\
    OrganizationUpdate, OrganizationInDBBase,\
    OrganizationTransferOwnership
from backend.schemas.organization_with_members import\
    OrganizationInDBBaseWithMembers
from backend.schemas.user_organization import\
    UserOrganizationCreate, UserOrganizationInDBBase
from backend.schemas.organization_subscription import\
    OrganizationSubscriptionCreate, OrganizationSubscriptionInDBBase
from backend.schemas.message import Message

router = APIRouter(
    prefix="/organization",
)


@router.get(
    "/",
    name="organization:get",
    response_model=list[OrganizationInDBBase],
    tags=["organization"]
)
def get_organizations(
    skip: int = 0,
    limit: int = 100,
    db=Depends(get_db),
):
    return crud.organization.get_multi(db, skip=skip, limit=limit)


@router.get(
    "/{organization_id}",
    name="organization:get_by_id",
    response_model=OrganizationInDBBaseWithMembers,
    tags=["organization"]
)
def get_organization_by_id(
    organization_id: int,
    db=Depends(get_db),
):
    organization = crud.organization.get_by_id_with_members(
        db, id=organization_id)

    if not organization:
        raise HTTPException(
            status_code=404,
            detail=strings.ORGANIZATION_DOES_NOT_FOUND_ERROR
        )
    return organization


@router.post(
    "/",
    name="organization:create",
    status_code=201,
    response_model=OrganizationInDBBase,
    dependencies=[Depends(user_exist)],
    tags=["organization"]
)
def create_organization(
    request: Request,
    organization_in: OrganizationCreate,
    db=Depends(get_db),
):
    return crud.organization.create_with_user(
        db, obj_in=organization_in,
        user_id=request.state.current_user.id)


@router.put(
    "/{organization_id}",
    name="organization:update",
    response_model=OrganizationInDBBase,
    dependencies=[Depends(user_exist)],
    tags=["organization"]
)
def update_organization(
    request: Request,
    organization_id: int,
    organization_in: OrganizationUpdate,
    db=Depends(get_db),
):
    organization = crud.organization.get(db, id=organization_id)

    if not organization:
        raise HTTPException(
            status_code=404,
            detail=strings.ORGANIZATION_DOES_NOT_FOUND_ERROR
        )

    user_organization = crud.user_organization.\
        get_by_user_and_organization(
            db, user_id=request.state.current_user.id,
            organization_id=organization.id
        )

    if not user_organization or not user_organization.is_owner:
        raise HTTPException(
            status_code=403,
            detail=strings.NOT_HAVE_PERMISSION_TO_UPDATE_THIS_ORGANIZATION
        )

    return crud.organization.update(
        db, db_obj=organization, obj_in=organization_in)


@router.delete(
    "/{organization_id}",
    name="organization:delete",
    response_model=Message,
    dependencies=[Depends(user_exist)],
    tags=["organization"]
)
def delete_organization(
    request: Request,
    organization_id: int,
    db=Depends(get_db),
):
    organization = crud.organization.get(db, id=organization_id)

    if not organization:
        raise HTTPException(
            status_code=404,
            detail=strings.ORGANIZATION_DOES_NOT_FOUND_ERROR
        )

    user_organization = crud.user_organization.\
        get_by_user_and_organization(
            db, user_id=request.state.current_user.id,
            organization_id=organization.id
        )

    if not user_organization or not user_organization.is_owner:
        raise HTTPException(
            status_code=403,
            detail=strings.NOT_HAVE_PERMISSION_TO_UPDATE_THIS_ORGANIZATION
        )

    crud.organization.remove(db, id=organization_id)

    return Message(
        detail=strings.ORGANIZATION_HAS_BEEN_DELETED
    )


@router.post(
    "/{organization_id}/member",
    name="organization_member:create",
    status_code=201,
    response_model=UserOrganizationInDBBase,
    dependencies=[Depends(user_exist)],
    tags=["organization member"]
)
def create_user_organization(
    request: Request,
    organization_id: int,
    user_id: int,
    db=Depends(get_db),
):
    organization = crud.organization.get(db, id=organization_id)

    if not organization:
        raise HTTPException(
            status_code=404,
            detail=strings.ORGANIZATION_DOES_NOT_FOUND_ERROR
        )

    user_organization = crud.user_organization.\
        get_by_user_and_organization(
            db, user_id=request.state.current_user.id,
            organization_id=organization.id
        )

    if not user_organization or not user_organization.is_owner:
        raise HTTPException(
            status_code=403,
            detail=strings.DO_NOT_HAVE_RIGHTS_TO_ADD_A_NEW_USER_TO_THE_ORGANIZATION
        )

    if crud.user_organization.\
            get_by_user_and_organization(
                db, user_id=user_id, organization_id=organization.id
            ):
        raise HTTPException(
            status_code=403,
            detail=strings.THE_USER_IS_ALREADY_A_MEMBER_OF_THE_ORGANIZATION
        )

    return crud.user_organization.create(
        db, obj_in=UserOrganizationCreate(
            user_id=user_id,
            organization_id=organization.id,
            is_owner=True
        ))


@router.delete(
    "/{organization_id}/member",
    name="organization_member:delete",
    response_model=UserOrganizationInDBBase,
    dependencies=[Depends(user_exist)],
    tags=["organization member"]
)
def delete_user_organization(
    request: Request,
    organization_id: int,
    user_id: int,
    db=Depends(get_db),
):
    organization = crud.organization.get(db, id=organization_id)

    if not organization:
        raise HTTPException(
            status_code=404,
            detail=strings.ORGANIZATION_DOES_NOT_FOUND_ERROR
        )

    user_organization = crud.user_organization.\
        get_by_user_and_organization(
            db, user_id=request.state.current_user.id,
            organization_id=organization.id
        )

    if not user_organization and not user_organization.is_owner:
        raise HTTPException(
            status_code=403,
            detail=strings.DO_NOT_HAVE_RIGHTS_TO_ADD_A_NEW_USER_TO_THE_ORGANIZATION
        )

    user_organization_2 = crud.user_organization.\
        get_by_user_and_organization(
            db, user_id=user_id, organization_id=organization.id
        )

    if not user_organization_2:
        raise HTTPException(
            status_code=409,
            detail=strings.THE_USER_IS_NOT_A_MEMBER_OF_THE_ORGANIZATION
        )

    if user_organization_2.is_owner:
        owner_count = crud.organization.get_count_owners(
            db, db_obj=organization)
        if owner_count == 1:
            raise HTTPException(
                status_code=400,
                detail=strings.CANNOT_REMOVE_YOURSELF_FROM_AN_ORGANIZATION_WHEN_NO_MORE_OWNERS
            )

    return crud.user_organization.remove(
        db, id=user_organization_2.id)


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


@router.post(
    "/{organization_id}/transfer-ownership",
    name="organization:transfer_ownership",
    response_model=Message,
    dependencies=[Depends(user_exist)],
    tags=["organization transfer ownership"],
)
def transfer_ownership(
    request: Request,
    organization_id: int,
    transwer_ownership_in: OrganizationTransferOwnership,
    db=Depends(get_db)
):
    organization = crud.organization.get(db, id=organization_id)

    if not organization:
        raise HTTPException(
            status_code=404,
            detail=strings.ORGANIZATION_DOES_NOT_FOUND_ERROR
        )

    user_organization_1 = crud.user_organization.\
        get_by_user_and_organization(
            db, user_id=request.state.current_user.id,
            organization_id=organization.id
        )

    if not user_organization_1 or not user_organization_1.is_owner:
        raise HTTPException(
            status_code=403,
            detail=strings.DO_NOT_HAVE_RIGHTS_TO_ADD_A_NEW_USER_TO_THE_ORGANIZATION
        )

    user_organization_2 = crud.user_organization.get_by_user_and_organization(
        db, user_id=transwer_ownership_in.user_id,
        organization_id=organization.id)
    if not user_organization_2:
        raise HTTPException(
            status_code=403,
            detail=strings.THE_USER_IS_ALREADY_A_MEMBER_OF_THE_ORGANIZATION
        )

    a, b = crud.user_organization.transfer_owner(
        db,
        user_organization_1=user_organization_1,
        user_organization_2=user_organization_2)
    print(a.is_owner, b.is_owner)

    return Message(
        detail="OK"
    )
