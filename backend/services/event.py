from backend.schemas.user import UserInDBBase
from backend.schemas.event import EventInDBBase
from backend.schemas.user_organization import UserOrganizationInDBBase


def check_user_can_create_event_by_organization(
    user_organization: UserOrganizationInDBBase
) -> bool:
    return user_organization is not None


def check_user_can_modify_event(
    user: UserInDBBase,
    event: EventInDBBase,
    user_organization: UserOrganizationInDBBase | None
) -> bool:
    return user_organization is not None or\
        user.is_admin is True or user.is_moderator is True or\
        (event.user.id == user.id and event.organization is None)
