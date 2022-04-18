from fastapi_azure_auth import SingleTenantAzureAuthorizationCodeBearer

from backend.config import settings

azure_scheme = SingleTenantAzureAuthorizationCodeBearer(
    app_client_id=settings.app_client_id,
    tenant_id=settings.tenant_id,
    scopes={
        f'api://{settings.app_client_id}/user_impersonation': 'user_impersonation',
    }
)

azure_scheme_without_error = SingleTenantAzureAuthorizationCodeBearer(
    app_client_id=settings.app_client_id,
    tenant_id=settings.tenant_id,
    scopes={
        f'api://{settings.app_client_id}/user_impersonation': 'user_impersonation',
    },
    auto_error=False
)
