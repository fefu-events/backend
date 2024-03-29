from fastapi import status
from pytest_cases import parametrize

from backend.resources import strings

from tests.utils import get_ids_ordered


def test_empty(client_app):
    response = client_app.get("/user/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data == []


def test_3_users(users, client_app):
    user_1, user_2, user_3 = users
    response = client_app.get("/user/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert [user_1.id, user_2.id, user_3.id] == get_ids_ordered(data)


def test_search_query(users, client_app):
    user_1, user_2, user_3 = users
    response = client_app.get("/user/?search_query=And")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert [user_1.id] == get_ids_ordered(data)

    response = client_app.get("/user/?search_query=gmail")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert [user_2.id, user_3.id] == get_ids_ordered(data)


@parametrize("i_user", range(0, 3))
def test_user_by_id(users, i_user, client_app):
    response = client_app.get(f"/user/{users[i_user].id}/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['id'] == users[i_user].id
    assert data['name'] == users[i_user].name
    assert data['email'] == users[i_user].email
    assert data['tags'] == users[i_user].tags


def test_user_by_id_404(users, client_app):
    response = client_app.get("/user/10/")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == strings.USER_DOES_NOT_EXIST
