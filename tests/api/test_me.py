from fastapi import status

from backend.resources import strings

from tests.utils import get_random_user

def test_post_me_normal(client_app):
    user = get_random_user()
    response = client_app.post("/me/", headers=user.get_test_headers())
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data['name'] == user.name
    assert data['email'] == user.email
    assert data['tags'] == []


def test_post_me_already_exist(client_app):
    user = get_random_user()
    client_app.post("/me/", headers=user.get_test_headers())
    response = client_app.post("/me/", headers=user.get_test_headers())
    assert response.status_code == status.HTTP_409_CONFLICT
    data = response.json()
    assert data['detail'] == strings.EMAIL_TAKEN


def test_get_me_normal(client_app):
    user = get_random_user()
    client_app.post("/me/", headers=user.get_test_headers())
    response = client_app.get("/me/", headers=user.get_test_headers())
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['name'] == user.name
    assert data['email'] == user.email
    assert data['tags'] == []
