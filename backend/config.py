from pydantic import AnyHttpUrl, BaseSettings, Field


class Settings(BaseSettings):
    DATABASE_URL: str = Field(default='', env='DATABASE_URL')
    TEST_DATABASE_URL: str = Field(default='',
                                   env="TEST_DATABASE_URL")
    SECRET_KEY: str = Field('my super secret key', env='SECRET_KEY')
    BACKEND_CORS_ORIGINS: list[str | AnyHttpUrl] = [
        'http://localhost:8000', 'http://localhost:8080',
        'http://192.168.0.12:8080', "https://192.168.0.12:8080"
    ]

    # Azure ad
    OPENAPI_CLIENT_ID: str = Field(default='', env='OPENAPI_CLIENT_ID')
    APP_CLIENT_ID: str = Field(default='', env='APP_CLIENT_ID')
    TENANT_ID: str = Field(default='', env='TENANT_ID')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True


settings = Settings()
