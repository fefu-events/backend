import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from backend import crud
from backend.database.session import SessionLocal
from backend.schemas.category import CategoryCreate


db = SessionLocal()

categories = [
    {
        "label": "Официальное",
    },
    {
        "label": "Образование",
    },
    {
        "label": "Развлечения",
    },
    {
        "label": "Спорт",
    },
    {
        "label": "Другое",
    },
]

for category in categories:
    crud.category.create(db, obj_in=CategoryCreate(**category))
