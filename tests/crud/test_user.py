from backend import crud
from backend.schemas.user import UserAzure
from sqlalchemy.orm import Session


def test_get_all_users_empty(db: Session) -> None:
    users = crud.user.get_multi(db, skip=0, limit=100)
    assert users == []


def test_create_user(db):
    obj_in = UserAzure(
        email="andrey@gmail.com",
        name="Andrey",
    )
    user = crud.user.create(db, obj_in=obj_in)
    assert user.email == obj_in.email
    assert user.name == obj_in.name
    assert not user.is_admin
    assert not user.is_moderator
    assert user.tags == []
