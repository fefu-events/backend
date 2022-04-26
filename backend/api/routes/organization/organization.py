from fastapi import APIRouter, Depends, HTTPException

from backend import crud
from backend.api.dependencies.database import get_db
from backend.api.dependencies.user import get_current_user
from backend.api.dependencies.organization import (
    get_organization_by_id_from_path
)
from backend.models.organization import Organization
from backend.schemas.organization import (
    OrganizationCreateWithMembers,
    OrganizationUpdate,
    OrganizationInDBBase,
)
from backend.schemas.organization_with_members import (
    OrganizationInDBBaseWithMembers
)
from backend.schemas.user import UserInDBBase
from backend.schemas.message import Message
from backend.services.organization import check_user_can_modify_organization
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
    "/{organization_id}/",
    name="organization:get_by_id",
    response_model=OrganizationInDBBaseWithMembers,
    tags=["organization"],
)
def get_organization_by_id(
    organization: OrganizationInDBBase =
        Depends(get_organization_by_id_from_path),
):
    return organization


@router.post(
    "/",
    name="organization:create",
    status_code=201,
    response_model=OrganizationInDBBase,
    tags=["organization"],
)
def create_organization(
    organization_in: OrganizationCreateWithMembers,
    current_user: UserInDBBase = Depends(get_current_user()),
    db=Depends(get_db),
):
    for member_id in organization_in.members_ids:
        user = crud.user.get(db, member_id)
        if not user:
            raise HTTPException(
                status_code=409,
                detail=strings.USER_DOES_NOT_EXIST,
            )

    return crud.organization.create_with_user(
        db, obj_in=organization_in,
        user_id=current_user.id
    )


@router.put(
    "/{organization_id}/",
    name="organization:update",
    response_model=OrganizationInDBBase,
    tags=["organization"],
)
def update_organization(
    organization_in: OrganizationUpdate,
    db=Depends(get_db),
    current_user: UserInDBBase = Depends(get_current_user()),
    organization: Organization = Depends(get_organization_by_id_from_path),
):
    if not check_user_can_modify_organization(
        crud.user_organization.get_by_user_and_organization(
            db, user_id=current_user.id,
            organization_id=organization.id)): # type: ignore
        raise HTTPException(
            status_code=403,
            detail=strings.CANNOT_MODIFY_ORGANIZATION
        )
    return crud.organization.update(
        db, db_obj=organization, obj_in=organization_in)


@router.delete(
    "/{organization_id}/",
    name="organization:delete",
    response_model=Message,
    tags=["organization"],
)
def delete_organization(
    db=Depends(get_db),
    current_user: UserInDBBase = Depends(get_current_user()),
    organization: OrganizationInDBBase =
        Depends(get_organization_by_id_from_path),
):
    if not check_user_can_modify_organization(
        crud.user_organization.get_by_user_and_organization(
            db, user_id=current_user.id,
            organization_id=organization.id)):
        raise HTTPException(
            status_code=403,
            detail=strings.CANNOT_MODIFY_ORGANIZATION
        )
    crud.organization.remove(db, id=organization.id)
    return Message(detail=strings.ORGANIZATION_HAS_BEEN_DELETED)
