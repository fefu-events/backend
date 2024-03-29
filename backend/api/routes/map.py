from datetime import datetime

from fastapi import APIRouter, Depends, Query, HTTPException

from backend import crud
from backend.api.dependencies.database import get_db
from backend.resources import strings
from backend.schemas.place import PlaceForMapInDBBase
from backend.utils import prepare_search_input

router = APIRouter()


@router.get(
    "/",
    name="map:get",
    response_model=list[PlaceForMapInDBBase],
)
def get_me(
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
    if title:
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
    return crud.place.get_for_map(
        db, title=title,
        date_begin=date_begin, date_end=date_end, user_id=user_id,
        organization_id=organization_id, place_ids=place_ids,
        category_ids=category_ids, user=user, tags=tags,
        subscriptions=subscriptions,
        personalize_tags=personalize_tags,
        archived=archived
    )
