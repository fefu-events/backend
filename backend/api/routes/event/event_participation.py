from fastapi import (
    APIRouter, Depends, HTTPException, Request,
)

from backend import crud
from backend.resources import strings
from backend.api.dependencies.database import get_db
from backend.api.dependencies.user import (
    get_current_user
)
from backend.api.dependencies.event import (
    get_event_by_id_from_path
)
from backend.schemas.user import UserInDBBase
from backend.schemas.event import EventInDBBase
from backend.schemas.participation import ParticipationInDBBase
from backend.schemas.message import Message

router = APIRouter()


@router.post(
    '/{event_id}/participant/',
    name="event:create_participant",
    response_model=ParticipationInDBBase,
)
def create_participant(
    event: EventInDBBase = Depends(get_event_by_id_from_path),
    current_user: UserInDBBase = Depends(get_current_user()),
    db=Depends(get_db),
):
    participation = crud.participation.get_by_event_and_user(
        db, event_id=event.id, user_id=current_user.id)

    if participation:
        raise HTTPException(
            status_code=409,
            detail=strings.USER_IS_ALREADY_PARTICIPATED
        )

    return crud.participation.create_with_user(
        db, event_id=event.id, user_id=current_user.id)


@router.delete(
    '/{event_id}/participant/',
    name="event:delete_participant",
    response_model=Message,
)
def delete_participant(
    request: Request,
    event: EventInDBBase = Depends(get_event_by_id_from_path),
    current_user: UserInDBBase = Depends(get_current_user()),
    db=Depends(get_db),
):
    participation = crud.participation.get_by_event_and_user(
        db, event_id=event.id, user_id=current_user.id)

    if not participation:
        raise HTTPException(
            status_code=409,
            detail=strings.USER_IS_NOT_PARTICIPATING
        )

    crud.participation.remove(db, id=participation.id)
    return Message(detail=strings.USER_IS_NOT_PARTICIPATING)
