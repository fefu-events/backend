from fastapi import APIRouter, Depends, Request

from backend import crud
from backend.routers.dependencies import get_db, user_exist
from backend.schemas.organization import OrganizationCreate,\
    OrganizationInDBBase

router = APIRouter(
    prefix="/organization",
)


@router.post(
    "/",
    name="organization:create",
    status_code=201,
    response_model=OrganizationInDBBase,
    dependencies=[Depends(user_exist)],
    tags=["organization"]
)
def create_event(
    request: Request,
    organization_in: OrganizationCreate,
    db=Depends(get_db),
):
    return crud.organization.create_with_user(
        db, obj_in=organization_in,
        user_id=request.state.current_user.id)
