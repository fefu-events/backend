from fastapi import APIRouter

from backend.api.routes.user import user, user_following, user_set_access

router = APIRouter()

router.include_router(user.router,
                      tags=["user"],
                      prefix="/user")
router.include_router(user_following.router,
                      tags=["user following"],
                      prefix="/user")
router.include_router(user_set_access.router,
                      tags=["user access"],
                      prefix="/user")
