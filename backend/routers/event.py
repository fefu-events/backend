from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import RedirectResponse

from backend import crud
from backend.routers.dependencies import get_db, user_exist
from backend.schemas.event import EventCreate, EventInDBBase, EventUpdate
from backend.utils import encode_query_params

router = APIRouter(
    prefix="/event",
    tags=["event"],
)


@router.post(
    "/",
    name="event:create",
    response_model=EventInDBBase,
    dependencies=[Depends(user_exist)],
)
def create_event(
    request: Request,
    event_in: EventCreate,
    db=Depends(get_db),
):
    place = crud.place.get(db, id=event_in.place_id)
    if not place:
        raise HTTPException(
            status_code=404
        )
    category = crud.category.get(db, id=event_in.category_id)
    if not category:
        raise HTTPException(
            status_code=404
        )
    return crud.event.create_with_user(
        db, obj_in=event_in, user_id=request.state.current_user.id)


@router.put(
    "/{event_id}",
    name="event:update",
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
    name="event:delete",
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
    name="event:get_by_id",
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
    name="event:get",
    response_model=list[EventInDBBase],
    dependencies=[Depends(user_exist)],
)
def get_events(
    skip: int = 0,
    limit: int = 100,
    title: str = None,
    date_begin: datetime = None,
    date_end: datetime = None,
    tags: list[str] = Query(None),
    user_id: int = None,
    personalize_tags: bool = None,
    db=Depends(get_db),
):
    if personalize_tags:
        query_params = encode_query_params({
            "skip": skip,
            "limit": limit,
            "title": title,
            "date_begin": date_begin,
            "date_end": date_end,
            "tags": tags,
            "user_id": user_id
        })
        return RedirectResponse(
            f"/personal-events{query_params}",
            status_code=303,
        )
    events = crud.event.get_multi_with_filter(
        db, skip=skip, limit=limit, title=title,
        date_begin=date_begin, date_end=date_end, user_id=user_id,
        tags=tags)
    return events
