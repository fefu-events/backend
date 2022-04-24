import pytest

from fastapi import Header
from fastapi.testclient import TestClient

from backend.schemas.user import UserAzure, UserInDBBase
from backend.api.dependencies.user import (
    get_user_azure,
    get_current_user
)
from main import app


@pytest.fixture(autouse=True)
def client_app():
    client = TestClient(app)

    def get_current_user_overrided(required=True):
        def get_current_user_overrided_required(
            authoriozation: str = Header(default=""),
        ):
            name, email = authoriozation.split(':')
            return UserAzure(
                name=name,
                email=email
            )

        return get_current_user_overrided_required

    app.dependency_overrides[get_current_user] = get_current_user_overrided()
    app.dependency_overrides[get_user_azure] = get_current_user_overrided(
        required=True
    )

    yield client


@pytest.fixture
def users(client_app) -> list[UserInDBBase]:
    users = [
        UserAzure(name="Andrey", email="andrey.va@yandex.ru"),
        UserAzure(name="Tom", email="cruise@gmail.com"),
        UserAzure(name="Jack", email="trololololo@gmail.com")
    ]
    return [
        UserInDBBase(
            **client_app.post("/me/", headers=user.get_test_headers()).json()
        )
        for user in users
    ]
