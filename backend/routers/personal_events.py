from datetime import datetime

from fastapi import APIRouter, Depends, Query, Request

from backend import crud
from backend.routers.dependencies import get_db, user_exist
from backend.schemas.event import EventInDBBase

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
    personalize_tags: bool = True,
    db=Depends(get_db),
):
    events = crud.event.get_multi_with_filter(
        db, skip=skip, limit=limit, title=title,
        date_begin=date_begin, date_end=date_end, user_id=user_id,
        tags=tags, user_tags=request.state.current_user.tags)
    return events
