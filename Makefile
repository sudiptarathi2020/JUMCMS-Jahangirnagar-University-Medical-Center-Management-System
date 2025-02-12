install:
	poetry install


migrate:
	poetry run python jumcms/manage.py migrate


migrations:
	poetry run python jumcms/manage.py makemigration

run-server:
	poetry run python jumcms/manage.py runserver


