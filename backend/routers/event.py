from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query,\
    Request

from backend import crud
from backend.resources import strings
from backend.routers.dependencies import get_db, user_exist
from backend.schemas.event import EventCreate, EventInDBBase, EventUpdate
from backend.schemas.participation import ParticipationInDBBase
from backend.schemas.message import Message
from backend.utils import prepare_search_input

router = APIRouter(
    prefix="/event",
)


@router.post(
    "/",
    name="event:create",
    status_code=201,
    response_model=EventInDBBase,
    dependencies=[Depends(user_exist)],
    tags=["event"],
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

    if event_in.organization_id is not None:
        organization = crud.organization.get(
            db, id=event_in.organization_id)

        if not organization:
            raise HTTPException(
                status_code=409,
                detail=strings.ORGANIZATION_DOES_NOT_FOUND_ERROR
            )

        user_organization = crud.user_organization.\
            get_by_user_and_organization(
                db, user_id=request.state.current_user.id,
                organization_id=organization.id
            )

        if not user_organization or not user_organization.is_owner:
            raise HTTPException(
                status_code=403,
                detail=strings.NOT_HAVE_PERMISSION_TO_POST_BY_THIS_ORGANIZATION
            )

    return crud.event.create_with_user(
        db, obj_in=event_in, user_id=request.state.current_user.id)


@router.put(
    "/{event_id}",
    name="event:update",
    response_model=EventInDBBase,
    dependencies=[Depends(user_exist)],
    tags=["event"],
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
    tags=["event"],
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
    if event.organization_id is not None:
        organization = crud.organization.get(
            db, id=event.organization_id)

        user_organization = crud.user_organization.\
            get_by_user_and_organization(
                db, user_id=request.state.current_user.id,
                organization_id=organization.id
            )

        if not user_organization:
            raise HTTPException(
                status_code=403,
                detail=strings.EVENT_DOES_NOT_HAVE_RIGHT_TO_DELETE_ERROR
            )
    else:
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
    tags=["event"],
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
    tags=["event"],
)
def get_events(
    skip: int = 0,
    limit: int = 100,
    title: str = None,
    date_begin: datetime = None,
    date_end: datetime = None,
    tags: list[str] = Query(None),
    user_id: int = None,
    organization_id: int = None,
    category_ids: list[int] = Query(None),
    place_ids: list[int] = Query(None),
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
        organization_id=organization_id, place_ids=place_ids,
        category_ids=category_ids, user=user, tags=tags,
        subscriptions=subscriptions,
        personalize_tags=personalize_tags)
    return events


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
