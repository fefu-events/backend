from fastapi import APIRouter, Depends, HTTPException, Request

from backend import crud
from backend.resources import strings
from backend.routers.dependencies import user_exist, get_db
from backend.schemas.category import CategoryInDBBase

router = APIRouter(
    prefix="/category",
    tags=["category"],
)


@router.get(
    "/",
    name="category:get",
    response_model=list[CategoryInDBBase],
)
def get_me(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    db=Depends(get_db),
):
    return crud.category.get_multi(db, skip=skip, limit=limit)
