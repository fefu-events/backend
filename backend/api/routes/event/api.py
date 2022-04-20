from fastapi import APIRouter

from backend.api.routes.event import (
    event,
    event_participation
)


router = APIRouter()

router.include_router(event.router,
                      prefix="/event",
                      tags=["event"])
router.include_router(event_participation.router,
                      prefix="/event",
                      tags=["event participation"])
