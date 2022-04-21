from fastapi import APIRouter

from backend.api.routes import (
    current_user_exist,
    me,
    place,
    category,
    map,
    image
)
from backend.api.routes.user import api as user
from backend.api.routes.organization import api as organization
from backend.api.routes.event import api as event

router = APIRouter()

router.include_router(
    current_user_exist.router,
    tags=["current user exist"],
    prefix="/current-user-exist",
)
router.include_router(
    me.router,
    tags=["me"],
    prefix="/me",
)
router.include_router(
    user.router,
)
router.include_router(
    organization.router,
)
router.include_router(
    event.router,
)
router.include_router(
    place.router,
    prefix="/place",
    tags=["place"]
)
router.include_router(
    category.router,
    prefix="/category",
    tags=["category"]
)
router.include_router(
    map.router,
    prefix="/map",
    tags=["map"],
)
router.include_router(
    image.router,
    prefix="/image",
    tags=["image"],
)
