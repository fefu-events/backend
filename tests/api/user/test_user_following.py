from fastapi import status

from backend.resources import strings
from pytest_cases import parametrize

from tests.utils import get_ids_ordered


@parametrize("i_user", range(0, 2))
def test_follow_normal(users, i_user, client_app):
    follower = users[i_user]
    user = users[i_user + 1]
    response = client_app.post(f"/user/{user.id}/follow",
                               headers=follower.get_test_headers())
    response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data == {"user_id": user.id, "follower_id": follower.id}


def test_follow_yourself(users, client_app):
    follower = users[0]
    user = users[0]
    response = client_app.post(f"/user/{user.id}/follow",
                               headers=follower.get_test_headers())
    response.status_code == status.HTTP_400_BAD_REQUEST
    data = response.json()
    assert data['detail'] == strings.UNABLE_TO_FOLLOW_YOURSELF


def test_follow_already(users, client_app):
    follower = users[0]
    user = users[1]
    client_app.post(f"/user/{user.id}/follow",
                    headers=follower.get_test_headers())
    response = client_app.post(f"/user/{user.id}/follow",
                               headers=follower.get_test_headers())
    response.status_code == status.HTTP_409_CONFLICT
    data = response.json()
    assert data['detail'] == strings.USER_IS_ALREADY_FOLLOWED


@parametrize("i_user", range(0, 2))
def test_unfollow_normal(users, i_user, client_app):
    follower = users[i_user]
    user = users[i_user + 1]
    client_app.post(f"/user/{user.id}/follow",
                    headers=follower.get_test_headers())
    response = client_app.delete(f"/user/{user.id}/unfollow",
                                 headers=follower.get_test_headers())
    response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["detail"] == strings.USER_IS_NOT_FOLLOWED


@parametrize("i_user", range(0, 2))
def test_unfollow_not_followed(users, i_user, client_app):
    follower = users[i_user]
    user = users[i_user + 1]
    response = client_app.delete(f"/user/{user.id}/unfollow",
                                 headers=follower.get_test_headers())
    response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["detail"] == strings.USER_IS_NOT_FOLLOWED


@parametrize("i_user", range(0, 3))
def test_empty_followers(users, i_user, client_app):
    response = client_app.get(f"/user/{users[i_user].id}/followers",
                              headers=users[i_user].get_test_headers())
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data == []


def test_followers_normal(users, client_app):
    user = users[0]
    users_ids = []
    for user_i in users:
        if user_i == user:
            continue
        users_ids.append(user_i.id)
        client_app.post(f"/user/{user.id}/follow",
                        headers=user_i.get_test_headers())
    response = client_app.get(f"/user/{user.id}/followers")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    users_ids.sort()
    assert get_ids_ordered(data) == users_ids


@parametrize("i_user", range(0, 3))
def test_empty_following(users, i_user, client_app):
    response = client_app.get(f"/user/{users[i_user].id}/following",
                              headers=users[i_user].get_test_headers())
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data == []


def test_following(users, client_app):
    user = users[0]
    for user_i in users:
        if user_i is user:
            continue
        client_app.post(f"/user/{user.id}/follow",
                        headers=user_i.get_test_headers())
    for user_i in users:
        if user_i is user:
            continue
        response = client_app.get(f"/user/{user_i.id}/following")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert get_ids_ordered(data) == [user.id]
