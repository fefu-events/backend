from pydantic import BaseSettings, Field, AnyHttpUrl


class Settings(BaseSettings):
    DATABASE_URL: str = Field(default='', env='DATABASE_URL')
    SECRET_KEY: str = Field('my super secret key', env='SECRET_KEY')
    BACKEND_CORS_ORIGINS: list[str | AnyHttpUrl] = ['http://localhost:8000']

    # Azure ad
    OPENAPI_CLIENT_ID: str = Field(default='', env='OPENAPI_CLIENT_ID')
    APP_CLIENT_ID: str = Field(default='', env='APP_CLIENT_ID')
    TENANT_ID: str = Field(default='', env='TENANT_ID')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True


settings = Settings()
