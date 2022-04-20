from fastapi import APIRouter, Depends, HTTPException, Request

from backend import crud
from backend.api.dependencies.database import get_db
from backend.api.dependencies.user import get_current_user
from backend.api.dependencies.organization import (
    get_organization_by_id_from_path
)
from backend.schemas.user import UserInDBBase
from backend.schemas.organization import (
    OrganizationInDBBase,
    OrganizationTransferOwnership,
)
from backend.schemas.message import Message
from backend.services.organization import check_user_can_modify_organization
from backend.resources import strings

router = APIRouter()


@router.post(
    "/{organization_id}/transfer-ownership",
    name="organization:transfer_ownership",
    response_model=Message,
)
def transfer_ownership(
    transwer_ownership_in: OrganizationTransferOwnership,
    db=Depends(get_db),
    current_user: UserInDBBase = Depends(get_current_user()),
    organization: OrganizationInDBBase =
        Depends(get_organization_by_id_from_path),
):
    user_organization_1 = crud.user_organization.\
        get_by_user_and_organization(
            db, user_id=current_user.id,
            organization_id=organization.id
        )

    if not check_user_can_modify_organization(user_organization_1):
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

    crud.user_organization.transfer_owner(
        db, user_organization_1=user_organization_1,
        user_organization_2=user_organization_2)

    return Message(detail="OK")
