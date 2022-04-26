from fastapi import APIRouter, Depends, HTTPException, status

from backend import crud
from backend.api.dependencies.database import get_db
from backend.api.dependencies.user import get_current_user
from backend.api.dependencies.organization import (
    get_organization_by_id_from_path
)
from backend.models.organization import Organization
from backend.schemas.user import UserInDBBase
from backend.schemas.organization import (
    OrganizationInDBBase,
)
from backend.resources import strings

router = APIRouter()


@router.post(
    "/{organization_id}/verification/",
    name="organization:verification",
    response_model=OrganizationInDBBase,
)
def verify_organization(
    db=Depends(get_db),
    current_user: UserInDBBase = Depends(get_current_user()),
    organization: Organization =
        Depends(get_organization_by_id_from_path),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.CANNOT_MODIFY_ORGANIZATION
        )

    crud.organization.verify(db, db_obj=organization)
    return organization


@router.delete(
    "/{organization_id}/verification/",
    name="organization:delete verification",
    response_model=OrganizationInDBBase,
)
def unverify_organization(
    db=Depends(get_db),
    current_user: UserInDBBase = Depends(get_current_user()),
    organization: Organization =
        Depends(get_organization_by_id_from_path),
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.CANNOT_MODIFY_ORGANIZATION
        )

    crud.organization.verify(db, db_obj=organization, value=False)
    return organization
