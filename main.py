from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers.authentication import azure_scheme
from backend.config import settings

from backend.routers.current_user_exist import router as\
    current_user_exist_router
from backend.routers.user import router as user_router
from backend.routers.event import router as event_router
from backend.routers.me import router as me_router
from backend.routers.place import router as place_router
from backend.routers.category import router as category_router
from backend.routers.organization import router as\
    organization_router
from backend.routers.map import router as\
    map_router


settings.configure_logging()
app = FastAPI(**settings.fastapi_kwargs)


if settings.allowed_hosts:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


@app.on_event('startup')
async def load_config() -> None:
    """
    Load OpenID config on startup.
    """
    await azure_scheme.openid_config.load_config()

app.include_router(current_user_exist_router)
app.include_router(me_router)
app.include_router(user_router)
app.include_router(organization_router)
app.include_router(event_router)
app.include_router(place_router)
app.include_router(map_router)
app.include_router(category_router)
