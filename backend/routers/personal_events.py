from datetime import datetime

from fastapi import APIRouter, Depends, Query, Request

from backend import crud
from backend.routers.dependencies import get_db, user_exist
from backend.schemas.event import EventInDBBase
from backend.utils import prepare_search_input

router = APIRouter(
    prefix="/personal-events",
    tags=["personal-events"],
)


@router.get(
    "/",
    name="personal_events:get",
    dependencies=[Depends(user_exist)],
    response_model=list[EventInDBBase],
)
def get_events(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    title: str = None,
    date_begin: datetime = None,
    date_end: datetime = None,
    tags: list[str] = Query(None),
    user_id: int = None,
    subscriptions: bool = True,
    personalize_tags: bool = True,
    db=Depends(get_db),
):
    if title:
        title, tags_from_title = prepare_search_input(title)
        tags = tags + tags_from_title if tags else tags_from_title
    events = crud.event.get_multi_with_filter(
        db, skip=skip, limit=limit, title=title,
        date_begin=date_begin, date_end=date_end, user_id=user_id,
        tags=tags, user=request.state.current_user,
        subscriptions=subscriptions,
        personalize_tags=personalize_tags)
    return events
