from fastapi import APIRouter, Depends, HTTPException, Request

from backend import crud
from backend.resources import strings
from backend.routers.dependencies import user_exist, get_db
from backend.schemas.place import PlaceInDBBase

router = APIRouter(
    prefix="/place",
    tags=["place"],
)


@router.get(
    "/",
    name="place:get",
    response_model=list[PlaceInDBBase],
)
def get_me(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    db=Depends(get_db),
):
    return crud.place.get_multi(db, skip=skip, limit=limit)
