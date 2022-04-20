from fastapi import (
    APIRouter, Depends, HTTPException,
    Request,
)

from backend import crud
from backend.resources import strings
from backend.api.dependencies.database import get_db
from backend.api.dependencies.user import (
    user_exist,
)
from backend.schemas.participation import ParticipationInDBBase
from backend.schemas.message import Message

router = APIRouter()


@router.post(
    '/{event_id}/participant',
    name="event:create_participant",
    response_model=ParticipationInDBBase,
    dependencies=[Depends(user_exist)],
    tags=["participant"],
)
def create_participant(
    request: Request,
    event_id: int,
    db=Depends(get_db),
):
    event = crud.event.get(db, id=event_id)

    if not event:
        raise HTTPException(
            status_code=409,
            detail=strings.EVENT_DOES_NOT_EXIST_ERROR
        )

    participation = crud.participation.get_by_event_and_user(
        db, event_id=event_id, user_id=request.state.current_user.id)

    if participation:
        raise HTTPException(
            status_code=409,
            detail=strings.ARE_ALREADY_PARTICIPATING_IN_THE_EVENT_ERROR
        )

    return crud.participation.create_with_user(
        db, event_id=event_id, user_id=request.state.current_user.id)


@router.delete(
    '/{event_id}/participant',
    name="event:delete_participant",
    response_model=Message,
    dependencies=[Depends(user_exist)],
    tags=["participant"],
)
def delete_participant(
    request: Request,
    event_id: int,
    db=Depends(get_db),
):
    event = crud.event.get(db, id=event_id)

    if not event:
        raise HTTPException(
            status_code=409,
            detail=strings.EVENT_DOES_NOT_EXIST_ERROR
        )

    participation = crud.participation.get_by_event_and_user(
        db, event_id=event_id,
        user_id=request.state.current_user.id)

    if not participation:
        raise HTTPException(
            status_code=409,
            detail=strings.PARTICIPATION_DOES_NOT_EXIST_ERROR
        )

    crud.participation.remove(
        db, id=participation.id)
    return Message(
        detail=strings.ARE_NOT_PARTICIPATING
    )
