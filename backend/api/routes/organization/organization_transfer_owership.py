from fastapi import APIRouter, Depends, HTTPException, Request

from backend import crud
from backend.api.dependencies.database import get_db
from backend.api.dependencies.user import user_exist
from backend.schemas.organization import (
    OrganizationTransferOwnership
)
from backend.schemas.message import Message
from backend.resources import strings

router = APIRouter()


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
