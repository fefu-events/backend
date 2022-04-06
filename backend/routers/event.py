from fastapi import APIRouter, Depends, HTTPException, Request

from backend import crud
from backend.resources import strings
from backend.routers.dependencies import get_db, get_user_azure, user_exist
from backend.schemas.user import UserAzure, UserUpdate, UserInDBBase
from backend.schemas.event import EventBase, EventCreate, EventInDBBase


router = APIRouter(
    prefix="/event",
    tags=["event"],
)


@router.post(
    "/create",
    response_model=EventInDBBase,
    dependencies=[Depends(user_exist)],
)
def create_event(
    request: Request,
    event_in: EventCreate,
    db=Depends(get_db),
):
    return crud.event.create_with_user(
        db, obj_in=event_in, user_id=request.state.current_user.id)
