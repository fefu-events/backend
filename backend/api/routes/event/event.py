from datetime import datetime

from fastapi import (
    APIRouter, Depends, HTTPException, Query,
)

from backend import crud
from backend.api.dependencies.database import get_db
from backend.api.dependencies.event import (
    get_event_by_id_from_path
)
from backend.api.dependencies.user import (
    get_current_user
)
from backend.models.event import Event
from backend.resources import strings
from backend.schemas.event import (
    EventCreate,
    EventInDBBase,
    EventUpdate,
    EventWithAmIParticipationInDBBase,
)
from backend.schemas.message import Message
from backend.schemas.user import UserInDBBase
from backend.services.event import (
    check_user_can_create_event_by_organization,
    check_user_can_modify_event
)
from backend.utils import prepare_search_input

router = APIRouter()


@router.post(
    "/",
    name="event:create",
    status_code=201,
    response_model=EventInDBBase,
    tags=["event"],
)
def create_event(
    event_in: EventCreate,
    db=Depends(get_db),
    current_user: UserInDBBase = Depends(get_current_user()),
):
    if not crud.place.get(db, id=event_in.place_id):
        raise HTTPException(
            status_code=422,
            detail=strings.PLACE_DOES_NOT_EXIST
        )
    if not crud.category.get(db, id=event_in.category_id):
        raise HTTPException(
            status_code=422,
            detail=strings.CATEGORY_DOES_NOT_EXIST
        )
    if event_in.organization_id:
        if not check_user_can_create_event_by_organization(
            crud.user_organization.get_by_user_and_organization(
                db, user_id=current_user.id,
                organization_id=event_in.organization_id)
        ):
            raise HTTPException(
                status_code=403,
                detail=strings.CANNOT_MODIFY_ORGANIZATION
            )
    return crud.event.create_with_user(
        db, obj_in=event_in, user_id=current_user.id)


@router.put(
    "/{event_id}/",
    name="event:update",
    response_model=EventInDBBase,
    tags=["event"],
)
def update_event(
    event_in: EventUpdate,
    event: Event = Depends(get_event_by_id_from_path),
    current_user: UserInDBBase = Depends(get_current_user()),
    db=Depends(get_db),
):
    if not check_user_can_modify_event(
        current_user,
        event,
        crud.user_organization.get_by_user_and_organization(
            db, user_id=current_user.id, organization_id=event.organization.id
        ) if event.organization else None
    ):
        raise HTTPException(
            status_code=403,
            detail=strings.CANNOT_MODIFY_ORGANIZATION
        )
    return crud.event.update(db=db, db_obj=event, obj_in=event_in)


@router.delete(
    "/{event_id}/",
    name="event:delete",
    response_model=Message,
    tags=["event"],
)
def delete_event(
    event_id,
    event: EventInDBBase = Depends(get_event_by_id_from_path),
    current_user: UserInDBBase = Depends(get_current_user()),
    db=Depends(get_db),
):
    if not check_user_can_modify_event(
        current_user,
        event,
        crud.user_organization.get_by_user_and_organization(
            db, user_id=current_user.id, organization_id=event.organization.id
        ) if event.organization else None
    ):
        raise HTTPException(
            status_code=403,
            detail=strings.CANNOT_MODIFY_ORGANIZATION
        )
    crud.event.remove(db=db, id=event_id)
    return Message(detail=strings.EVENT_HAS_BEEN_DELETED)


@router.get(
    "/{event_id}/",
    name="event:get_by_id",
    response_model=EventWithAmIParticipationInDBBase,
    tags=["event"],
)
def get_event(
    event: EventInDBBase = Depends(get_event_by_id_from_path),
    current_user: UserInDBBase = Depends(get_current_user(required=False)),
    db=Depends(get_db),
):
    user_id = current_user.id if current_user else None
    result = EventWithAmIParticipationInDBBase.from_orm(event)
    result.am_i_participation = crud.participation.get_by_event_and_user(
        db, event_id=event.id, user_id=user_id
    ) is not None
    return result


@router.get(
    "/",
    name="event:get",
    response_model=list[EventInDBBase],
    tags=["event"],
)
def get_events(
    skip: int = 0,
    limit: int = 100,
    title: str | None = None,
    date_begin: datetime | None = None,
    date_end: datetime | None = None,
    tags: list[str] = Query(None, alias="tags[]"),
    user_id: int | None = None,
    organization_id: int | None = None,
    category_ids: list[int] = Query(None, alias="category_ids[]"),
    place_ids: list[int] = Query(None, alias="place_ids[]"),
    for_user_id: int | None = None,
    subscriptions: bool = False,
    personalize_tags: bool = False,
    archived: bool | None = False,
    db=Depends(get_db),
):
    if title:  # noqa
        title, tags_from_title = prepare_search_input(title)
        tags = tags + tags_from_title if tags else tags_from_title
    user = None
    if for_user_id:
        user = crud.user.get(db, id=for_user_id)
        if not user:
            raise HTTPException(
                status_code=409,
                detail=strings.USER_DOES_NOT_EXIST
            )
    events = crud.event.get_multi_with_filter(
        db, skip=skip, limit=limit, title=title,
        date_begin=date_begin, date_end=date_end, user_id=user_id,
        organization_id=organization_id, place_ids=place_ids,
        category_ids=category_ids, user=user, tags=tags,
        subscriptions=subscriptions,
        personalize_tags=personalize_tags,
        archived=archived)
    return events
