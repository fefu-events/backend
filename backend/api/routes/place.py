from fastapi import APIRouter, Depends, Request

from backend import crud
from backend.api.dependencies.database import get_db
from backend.schemas.place import PlaceInDBBase

router = APIRouter()


@router.get(
    "/",
    name="place:get",
    response_model=list[PlaceInDBBase],
)
def get_places(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    db=Depends(get_db),
):
    return crud.place.get_multi(db, skip=skip, limit=limit)
