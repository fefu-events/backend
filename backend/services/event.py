from backend.models.user import User
from backend.models.event import Event
from backend.models.user_organization import UserOrganization


def check_user_can_create_event_by_organization(
    user_organization: UserOrganization
) -> bool:
    return user_organization is not None


def check_user_can_modify_event(
    user: User, event: Event, user_organization: UserOrganization
) -> bool:
    return user_organization is not None or\
        user.is_admin or user.is_moderator or\
        event.user_id == user.id
