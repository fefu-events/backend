from fastapi import APIRouter, Depends

from backend import crud
from backend.api.dependencies.database import get_db
from backend.schemas.category import CategoryInDBBase

router = APIRouter()


@router.get(
    "/",
    name="category:get",
    response_model=list[CategoryInDBBase],
)
def get_me(
    skip: int = 0,
    limit: int = 100,
    db=Depends(get_db),
):
    return crud.category.get_multi(db, skip=skip, limit=limit)
