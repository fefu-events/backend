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

# https://stackoverflow.com/questions/2214575/passing-arguments-to-make-run
ifeq (provide_admin_rights,$(firstword $(MAKECMDGOALS)))
  provide_admin_rights_args := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(provide_admin_rights_args):;@:)
endif

provide_admin_rights:
	poetry run python $(SCRIPTS)/provide_admin_rights.py $(provide_admin_rights_args)