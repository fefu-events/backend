from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request

from backend import crud
from backend.routers.dependencies import get_db, user_exist
from backend.schemas.event import EventCreate, EventUpdate, EventInDBBase


router = APIRouter(
    prefix="/event",
    tags=["event"],
)


@router.post(
    "/",
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


@router.put(
    "/{event_id}",
    response_model=EventInDBBase,
    dependencies=[Depends(user_exist)],
)
def update_event(
    request: Request,
    event_id: int,
    event_in: EventUpdate,
    db=Depends(get_db),
):
    event = crud.event.get(db, id=event_id)

    if not event:
        raise HTTPException(
            status_code=404
        )

    if request.state.current_user.id != event.user_id:
        raise HTTPException(
            status_code=403
        )
    return crud.event.update(db=db, db_obj=event, obj_in=event_in)


@router.delete(
    "/{event_id}",
    response_model=EventInDBBase,
    dependencies=[Depends(user_exist)],
)
def delete_event(
    request: Request,
    event_id,
    db=Depends(get_db),
):
    event = crud.event.get(db, id=event_id)

    if not event:
        raise HTTPException(
            status_code=404
        )

    if not request.state.current_user.is_admin and\
            not request.state.current_user.is_moderator and\
            (request.state.current_user.id != event.user_id):
        raise HTTPException(
            status_code=403
        )
    return crud.event.remove(db=db, id=event_id)


@router.get(
    "/{event_id}",
    response_model=EventInDBBase,
)
def get_event(
    event_id: int,
    db=Depends(get_db),
):
    event = crud.event.get(db, id=event_id)

    if not event:
        raise HTTPException(
            status_code=404
        )
    return event


@router.get(
    "/",
    response_model=List[EventInDBBase],
)
def get_events(
    skip: int = 0,
    limit: int = 100,
    db=Depends(get_db)
):
    events = crud.event.get_multi(db, skip=skip, limit=limit)
    return events
