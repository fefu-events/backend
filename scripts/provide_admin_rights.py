import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from backend import crud  # noqa
from backend.resources import strings  # noqa
from backend.database.session import SessionLocal  # noqa

if len(sys.argv) > 2:
    print("Too many arguments", file=sys.stderr)
    exit(1)

db = SessionLocal()

user = crud.user.get_by_email(db, sys.argv[1])

if not user:
    print(strings.USER_DOES_NOT_EXIST, file=sys.stderr)
    exit(1)

crud.user.provide_admin_rights(db, user)

print("OK")
