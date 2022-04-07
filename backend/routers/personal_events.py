from typing import List
from datetime import datetime

from fastapi import APIRouter, Depends, Request, Query

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
    response_model=List[EventInDBBase],
)
def get_events(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    title: str = None,
    date_begin: datetime = None,
    date_end: datetime = None,
    tags: List[str] = Query(None),
    user_id: int = None,
    personalize_tags: bool = None,
    db=Depends(get_db),
):
    tags_joint = request.state.current_user.tags + tags or []
    print(tags_joint)
    events = crud.event.get_multi_with_filter(
        db, skip=skip, limit=limit, title=title,
        date_begin=date_begin, date_end=date_end, user_id=user_id,
        tags=tags_joint)
    return events
