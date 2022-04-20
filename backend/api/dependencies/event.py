from fastapi import Depends, HTTPException, Path, status

from backend import crud
from backend.api.dependencies.database import get_db
from backend.schemas.event import EventInDBBase
from backend.resources import strings


def get_event_by_id_from_path(
    event_id: int = Path(..., ge=1),
    db=Depends(get_db)
) -> EventInDBBase:
    event = crud.event.get(db, id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strings.EVENT_DOES_NOT_EXIST_ERROR,
        )
    return event
