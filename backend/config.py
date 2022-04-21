from enum import Enum
import logging
import sys

from loguru import logger
from pydantic import BaseSettings

from backend.logging import InterceptHandler


class AppEnvTypes(Enum):
    prod: str = "prod"
    dev: str = "dev"
    test: str = "test"


class BaseAppSettings(BaseSettings):
    app_env: AppEnvTypes = AppEnvTypes.test

    class Config:
        env_file = ".env"


class AppSettings(BaseAppSettings):
    debug: bool = False
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "FEFU Events backend"
    version: str = "0.0.0"

    database_url: str

    secret_key: str
    allowed_hosts: list[str] = ["*"]

    logging_hosts: int = logging.INFO
    loggers: tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")

    openapi_client_id: str
    app_client_id: str
    tenant_id: str

    dropbox_access_token: str
    dropbox_app_key: str
    dropbox_secret: str
    dropbox_refresh_token: str

    class Config:
        validate_assigment = True

    @property
    def fastapi_kwargs(self) -> dict[str, any]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version,
            "swagger_ui_oauth2_redirect_url": '/oauth2-redirect',
            "swagger_ui_init_oauth": {
                'usePkceWithAuthorizationCodeGrant': True,
                'clientId': self.openapi_client_id,
            },
        }

    @property
    def dropbox_kwargs(self) -> dict[str, any]:
        return {
            "oauth2_access_token": self.dropbox_access_token,
            "app_key": self.dropbox_app_key,
            "app_secret": self.dropbox_secret,
            "oauth2_refresh_token": self.dropbox_refresh_token
        }

    def configure_logging(self) -> None:
        logging.getLogger().handlers = [InterceptHandler()]
        for logger_name in self.loggers:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler(level=self.logging_level)]

        logger.configure(handlers=[{"sink": sys.stderr, "level": self.logging_level}])


class DevAppSettings(AppSettings):
    debug: bool = True

    title: str = "Dev FEFU Events backend"

    logging_level: int = logging.DEBUG

    class Config(AppSettings.Config):
        env_file = ".env.dev"


class ProdAppSettings(AppSettings):
    class Config(AppSettings.Config):
        env_file = ".env.prod"


class TestAppSettings(AppSettings):
    debug: bool = True

    title: str = "Test FEFU Events application"

    secret_key: str = "test"

    logging_level: int = logging.DEBUG

    class Config(AppSettings.Config):
        env_file = ".env.test"


environments: dict[AppEnvTypes, type[AppSettings]] = {
    AppEnvTypes.dev: DevAppSettings,
    AppEnvTypes.prod: ProdAppSettings,
    AppEnvTypes.test: TestAppSettings,
}

app_env = BaseAppSettings().app_env
settings = environments[app_env]()
