import string
import random
from datetime import datetime, timezone

from dateutil import tz
from dateutil.relativedelta import relativedelta

from backend.schemas.user import UserAzure
from backend.schemas.place import PlaceCreate
from backend.schemas.category import CategoryCreate


def get_random_str(length: int):
    return ''.join(random.choices(
        string.ascii_lowercase + string.digits, k=length))


def get_email(name):
    return f'{name}@gmail.com'


def get_random_user() -> UserAzure:
    name = get_random_str(length=10)
    return UserAzure(
        email=get_email(name),
        name=name,
    )


def get_random_place() -> PlaceCreate:
    return PlaceCreate(
        label=get_random_str(length=10),
        latitude=random.uniform(0, 100),
        longitude=random.uniform(0, 100),
    )


def get_random_category() -> CategoryCreate:
    return CategoryCreate(
        label=get_random_str(length=10),
    )


def get_ids_ordered(items):
    result = [item.id for item in items]
    result.sort()
    return result


def get_date_now() -> datetime:
    return datetime.now(timezone.utc)


def get_date_now_offset(
    years: int = 0, months: int = 0, days: int = 0, hours: int = 0
) -> datetime:
    return get_date_now() + relativedelta(
        years=years, months=months, days=days, hours=hours)


def get_date_now_offset_str(
    years: int = 0, months: int = 0, days: int = 0, hours: int = 0
) -> datetime:
    return convert_date_to_utz_with_z(get_date_now_offset(
        years=years, months=months, days=days, hours=hours))


def convert_date_to_utz_with_z(date: datetime) -> str:
    return date.strftime("%Y-%m-%dT%H:%M:%SZ")
