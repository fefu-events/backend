from backend.models.user_organization import UserOrganization


def check_user_can_modify_organization(
    user_organization: UserOrganization
) -> bool:
    return user_organization is not None and\
        user_organization.is_owner is True
