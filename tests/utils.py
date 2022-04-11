import string
import random

from backend.schemas.user import UserAzure


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


def get_ids_ordered(items):
    result = [item.id for item in items]
    result.sort()
    return result
