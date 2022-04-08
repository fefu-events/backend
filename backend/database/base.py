# Import all the models, so that Base has them before being
# imported by Alembic
from backend.database.base_class import Base  # noqa
from backend.models.event import Event
from backend.models.user import User
