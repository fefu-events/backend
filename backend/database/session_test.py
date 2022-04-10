from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.config import settings
from backend.database import base  # noqa: F401

# SQL Alchemy might fail to initialize properly relationships
# without this import


engine = create_engine(settings.TEST_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
