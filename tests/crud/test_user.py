from backend import crud
from backend.schemas.user import UserUpdate
from backend.schemas.user_subscription import UserSubscriptionCreate
from sqlalchemy.orm import Session

from tests.utils import get_random_user, get_ids_ordered


def test_get_all_users_empty(db: Session) -> None:
    users = crud.user.get_multi(db, skip=0, limit=100)
    assert users == []


def test_create_user(db):
    obj_in = get_random_user()
    user = crud.user.create(db, obj_in=obj_in)
    assert user.email == obj_in.email
    assert user.name == obj_in.name
    assert not user.is_admin
    assert not user.is_moderator
    assert user.tags == []


def test_update_user(db):
    user = crud.user.create(db, obj_in=get_random_user())
    tags = ["МОЛОДЕЖНОЕ", "соревнование"]
    crud.user.update(db, db_obj=user, obj_in=UserUpdate(
        tags=tags
    ))
    assert user.tags == tags


def test_get_by_email(db):
    user_1 = get_random_user()
    user_2 = get_random_user()

    crud.user.create(db, obj_in=user_1)
    crud.user.create(db, obj_in=user_2)

    user_db_1 = crud.user.get_by_email(db, email=user_1.email)
    user_db_2 = crud.user.get_by_email(db, email=user_2.email)

    assert user_db_1.email == user_1.email
    assert user_db_2.email == user_2.email

    assert user_db_1.name == user_1.name
    assert user_db_2.name == user_2.name


def test_following(db):
    user_1 = get_random_user()
    user_2 = get_random_user()
    user_3 = get_random_user()

    user_db_1 = crud.user.create(db, obj_in=user_1)
    user_db_2 = crud.user.create(db, obj_in=user_2)
    user_db_3 = crud.user.create(db, obj_in=user_3)

    crud.user_subscription.create(db, obj_in=UserSubscriptionCreate(
        follower_id=user_db_1.id,
        user_id=user_db_2.id
    ))

    assert [2] == get_ids_ordered(crud.user.get_following(
        db, user_id=user_db_1.id
    ))
    assert [] == get_ids_ordered(crud.user.get_followers(
        db, user_id=user_db_1.id
    ))
    assert [] == get_ids_ordered(crud.user.get_following(
        db, user_id=user_db_2.id
    ))
    assert [1] == get_ids_ordered(crud.user.get_followers(
        db, user_id=user_db_2.id
    ))

    crud.user_subscription.create(db, obj_in=UserSubscriptionCreate(
        follower_id=user_db_1.id,
        user_id=user_db_3.id
    ))

    assert [2, 3] == get_ids_ordered(crud.user.get_following(
        db, user_id=user_db_1.id
    ))

    assert [1] == get_ids_ordered(crud.user.get_followers(
        db, user_id=user_db_3.id
    ))
