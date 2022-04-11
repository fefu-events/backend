import pytest

from backend.database.session_test import SessionLocal, engine
from backend.database.base import Base


@pytest.fixture(autouse=True)
def db():
    Base.metadata.create_all(engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(engine)
