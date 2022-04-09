# Import all the models, so that Base has them before being
# imported by Alembic
from backend.database.base_class import Base  # noqa
from backend.models.category import Category  # noqa
from backend.models.event import Event  # noqa
from backend.models.place import Place  # noqa
from backend.models.user import User  # noqa
from backend.models.user_subscription import UserSubscription  # noqa
