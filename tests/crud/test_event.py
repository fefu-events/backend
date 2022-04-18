from sqlalchemy.orm import Session

from backend import crud
from backend.schemas.event import EventCreate, EventUpdate
from backend.schemas.user_subscription import UserSubscriptionCreate
from tests.utils import (
    get_random_user,
    get_random_place,
    get_random_category,
    get_date_now_offset_str
)


def test_create_event(db):
    user = crud.user.create(db, obj_in=get_random_user())

    place = crud.place.create(db, obj_in=get_random_place())
    category = crud.category.create(
        db, obj_in=get_random_category())

    event_data = EventCreate(
        title="По приколу собрались, калик покурить",
        description="Сказал же поприколу",
        date_begin=get_date_now_offset_str(days=10),
        date_end=get_date_now_offset_str(days=10, hours=2),
        place_description="",
        tags=["калик"],
        place_id=place.id,
        category_id=category.id,
    )

    event = crud.event.create_with_user(db, obj_in=event_data,
                                        user_id=user.id)
    assert event.title == event_data.title
    assert event.description == event_data.description
    assert event.date_begin == event_data.date_begin
    assert event.date_end == event_data.date_end
    assert event.place_description == event_data.place_description
    assert event.tags == event_data.tags
    assert event.place.id == place.id
    assert event.user.id == user.id
