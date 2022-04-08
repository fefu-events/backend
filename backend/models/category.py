from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from backend.database.base_class import Base


class Category(Base):
    id = Column(Integer, primary_key=True, index=True)
    label = Column(String(15), nullable=False)
    events = relationship("Event", back_populates="category")
