from fastapi import Depends, HTTPException, Path, status

from backend import crud
from backend.api.dependencies.database import get_db
from backend.schemas.organization import OrganizationInDBBase
from backend.resources import strings


def get_organization_by_id_from_path(
    organization_id: int = Path(..., ge=1),
    db=Depends(get_db)
) -> OrganizationInDBBase:
    organization = crud.organization.get(db, id=organization_id)
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strings.ORGANIZATION_DOES_NOT_FOUND_ERROR,
        )
    return organization
