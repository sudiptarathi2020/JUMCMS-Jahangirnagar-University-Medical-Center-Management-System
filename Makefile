.PHONY: install
install:
	poetry install

.PHONY: migrate
migrate:
	poetry run python jumcms/manage.py migrate

.PHONY: migrations
migrations:
	poetry run python jumcms/manage.py makemigration

.PHONY: run-server
run-server:
	poetry run python jumcms/manage.py runserver

.PHONY: superuser
superuser:
	poetry run python jumcms/manage.py createsuperuser

.PHONY: update
update: install migrate;
