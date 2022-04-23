from fastapi import status

from tests.utils import get_random_user


def test_not_exist(client_app):
    user = get_random_user()
    response = client_app.get("/current-user-exist/",
                              headers=user.get_test_headers())
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert not data["exist"]


def test_exist(client_app):
    user = get_random_user()
    client_app.post("/me/", headers=user.get_test_headers())
    response = client_app.get("/current-user-exist/",
                              headers=user.get_test_headers())
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["exist"]
