from fastapi import APIRouter

from backend.api.routes.user import user, user_following

router = APIRouter()

router.include_router(user.router,
                      tags=["user"],
                      prefix="/user")
router.include_router(user_following.router,
                      tags=["user following"],
                      prefix="/user")
