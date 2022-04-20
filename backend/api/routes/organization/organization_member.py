from fastapi import APIRouter, Depends, HTTPException

from backend.resources import strings
from backend import crud
from backend.api.dependencies.database import get_db
from backend.api.dependencies.user import get_current_user
from backend.api.dependencies.organization import (
    get_organization_by_id_from_path
)
from backend.schemas.user import UserInDBBase
from backend.schemas.organization import OrganizationInDBBase
from backend.schemas.user_organization import (
    UserOrganizationCreate,
    UserOrganizationDelete,
    UserOrganizationInDBBase,
)

router = APIRouter()


@router.post(
    "/{organization_id}/member",
    name="organization_member:create",
    status_code=201,
    response_model=UserOrganizationInDBBase,
    tags=["organization member"]
)
def create_member_of_organization(
    user_id: int,
    current_user: UserInDBBase = Depends(get_current_user()),
    db=Depends(get_db),
    organization: OrganizationInDBBase =
        Depends(get_organization_by_id_from_path),
):
    if not crud.user.get(db, id=user_id):
        raise HTTPException(
            status_code=409,
            detail=strings.USER_DOES_NOT_EXIST_ERROR
        )

    if organization.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail=strings.DO_NOT_HAVE_RIGHTS_TO_ADD_A_NEW_USER_TO_THE_ORGANIZATION
        )

    if crud.user_organization.get_by_user_and_organization(
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
    tags=["organization member"]
)
def delete_member_of_organization(
    user_organization_in: UserOrganizationDelete,
    db=Depends(get_db),
    current_user: UserInDBBase = Depends(get_current_user()),
    organization: OrganizationInDBBase =
        Depends(get_organization_by_id_from_path),
):
    if not crud.user.get(db, id=user_organization_in.user_id):
        raise HTTPException(
            status_code=409,
            detail=strings.USER_DOES_NOT_EXIST_ERROR
        )

    if organization.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail=strings.DO_NOT_HAVE_RIGHTS_TO_ADD_A_NEW_USER_TO_THE_ORGANIZATION
        )

    user_organization_2 = crud.user_organization.\
        get_by_user_and_organization(
            db, user_id=user_organization_in.user_id,
            organization_id=organization.id)

    if not user_organization_2:
        raise HTTPException(
            status_code=409,
            detail=strings.THE_USER_IS_NOT_A_MEMBER_OF_THE_ORGANIZATION
        )

    if organization.owner_id == current_user.id and\
            user_organization_in.user_id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail=strings.CANNOT_REMOVE_YOURSELF_FROM_AN_ORGANIZATION_WHEN_NO_MORE_OWNERS
        )

    return crud.user_organization.remove(db, id=user_organization_2.id)
