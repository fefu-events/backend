from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query,\
    Request
from fastapi.responses import RedirectResponse

from backend import crud
from backend.resources import strings
from backend.routers.dependencies import get_db, user_exist
from backend.schemas.event import EventCreate, EventInDBBase, EventUpdate
from backend.schemas.participation import ParticipationCreate,\
    ParticipationInDBBase
from backend.schemas.message import Message
from backend.utils import encode_query_params, prepare_search_input

router = APIRouter(
    prefix="/event",
    tags=["event"],
)


@router.post(
    "/",
    name="event:create",
    status_code=201,
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
            status_code=422,
            detail=strings.PLACE_DOES_NOT_EXIST_ERROR
        )
    category = crud.category.get(db, id=event_in.category_id)
    if not category:
        raise HTTPException(
            status_code=422,
            detail=strings.CATEGORY_DOES_NOT_EXIST_ERROR
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
            status_code=404,
            detail=strings.EVENT_DOES_NOT_EXIST_ERROR
        )

    if request.state.current_user.id != event.user_id:
        raise HTTPException(
            status_code=403,
            detail=strings.EVENT_DOES_NOT_HAVE_RIGHT_TO_UPDATE
        )
    return crud.event.update(db=db, db_obj=event, obj_in=event_in)


@router.delete(
    "/{event_id}",
    name="event:delete",
    response_model=Message,
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
            status_code=404,
            detail=strings.EVENT_DOES_NOT_EXIST_ERROR
        )

    if not request.state.current_user.is_admin and\
            not request.state.current_user.is_moderator and\
            (request.state.current_user.id != event.user_id):
        raise HTTPException(
            status_code=403,
            detail=strings.EVENT_DOES_NOT_HAVE_RIGHT_TO_DELETE_ERROR
        )

    crud.event.remove(db=db, id=event_id)
    return Message(
        detail=strings.EVENT_HAS_BEEN_DELETED
    )


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
            status_code=404,
            detail=strings.EVENT_DOES_NOT_EXIST_ERROR
        )
    return event


@router.get(
    "/",
    name="event:get",
    response_model=list[EventInDBBase],
)
def get_events(
    skip: int = 0,
    limit: int = 100,
    title: str = None,
    date_begin: datetime = None,
    date_end: datetime = None,
    tags: list[str] = Query(None),
    user_id: int = None,
    for_user_id: int = None,
    subscriptions: bool = False,
    personalize_tags: bool = False,
    db=Depends(get_db),
):
    if title:
        title, tags_from_title = prepare_search_input(title)
        tags = tags + tags_from_title if tags else tags_from_title
    user = None
    if for_user_id:
        user = crud.user.get(db, id=for_user_id)
        if not user:
            raise HTTPException(
                status_code=409,
                detail=strings.USER_DOES_NOT_EXIST_ERROR
            )
    events = crud.event.get_multi_with_filter(
        db, skip=skip, limit=limit, title=title,
        date_begin=date_begin, date_end=date_end, user_id=user_id,
        user=user, tags=tags, subscriptions=subscriptions,
        personalize_tags=personalize_tags)
    return events


@router.post(
    '/{event_id}/take-part',
    name="event:take_part",
    response_model=ParticipationInDBBase,
    dependencies=[Depends(user_exist)],
)
def follow_user(
    request: Request,
    participation_in: ParticipationCreate,
    db=Depends(get_db),
):
    event = crud.event.get(db, id=participation_in.event_id)

    if not event:
        raise HTTPException(
            status_code=409,
            detail=strings.EVENT_DOES_NOT_EXIST_ERROR
        )

    participation = crud.participation.get_by_event_and_user(
        db, event_id=participation_in.event_id,
        user_id=request.state.current_user.id)

    if participation:
        raise HTTPException(
            status_code=409,
            detail=strings.ARE_ALREADY_PARTICIPATING_IN_THE_EVENT_ERROR
        )

    return crud.participation.create_with_user(
        db, obj_in=participation_in,
        user_id=request.state.current_user.id)
