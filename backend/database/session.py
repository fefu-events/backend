from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.config import settings
from backend.database import base  # noqa: F401

# SQL Alchemy might fail to initialize properly relationships
# without this import


engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
