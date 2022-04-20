from fastapi import APIRouter, Depends, HTTPException, Request

from backend import crud
from backend.api.dependencies.database import get_db
from backend.api.dependencies.user import user_exist
from backend.schemas.organization import (
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationInDBBase,
)
from backend.schemas.organization_with_members import (
    OrganizationInDBBaseWithMembers
)
from backend.schemas.message import Message
from backend.resources import strings


router = APIRouter()


@router.get(
    "/",
    name="organization:get",
    response_model=list[OrganizationInDBBase],
    tags=["organization"],
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
    tags=["organization"],
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
    tags=["organization"],
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
    tags=["organization"],
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
    tags=["organization"],
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
