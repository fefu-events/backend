from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.schemas.azure import azure_scheme
from backend.config import settings

from backend.api.routes.api import router


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

app.include_router(router)
