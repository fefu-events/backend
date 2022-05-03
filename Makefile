CODE = backend
SRC = .
TEST = tests
SCRIPTS = scripts

run: init_database
	poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload --workers 4

init_database:
	poetry run alembic upgrade head
	poetry run python $(SCRIPTS)/init_categories.py
	poetry run python $(SCRIPTS)/init_places.py