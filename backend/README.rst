Project Setup Instructions
==========================

This project uses Poetry for dependency management and a Makefile to simplify common tasks. Follow the steps below to set up the project locally.

Prerequisites
-------------

- **Python**: Ensure Python 3.8 or higher is installed.
- **Poetry**: Install Poetry by following the instructions at `https://python-poetry.org/docs/#installation`.
- **Make**: Ensure you have `make` installed (available by default on Unix-like systems; for Windows, use WSL or a tool like MinGW).

Setup Steps
-----------

1. **Clone the Repository**

   Clone the project repository to your local machine:

   .. code-block:: bash

      git clone https://github.com/sudiptarathi2020/JUMCMS-Jahangirnagar-University-Medical-Center-Management-System.git
      cd JUMCMS-Jahangirnagar-University-Medical-Center-Management-System

2. **Install Dependencies**

   Use the Makefile to install the project dependencies using Poetry:

   .. code-block:: bash

      make install

   This command runs `poetry install --no-root` to install all dependencies listed in `pyproject.toml`.

3. **Apply Database Migrations**

   Set up the database by applying migrations:

   .. code-block:: bash

      make migrate

   This command runs `poetry run python -m core.manage migrate` to apply all database migrations.

4. **(Optional) Create Database Migrations**

   If you need to generate new migrations for model changes:

   .. code-block:: bash

      make migrations

   This command runs `poetry run python -m core.manage makemigrations` to create new migration files.

5. **(Optional) Create a Superuser**

   To create an admin user for the Django admin interface:

   .. code-block:: bash

      make superuser

   This command runs `poetry run python -m core.manage createsuperuser` and prompts you to set up a superuser account.

6. **Run the Development Server**

   Start the development server to run the project locally:

   .. code-block:: bash

      make run-server

   This command runs `poetry run python -m core.manage runserver`, typically starting the server at `http://localhost:8000`.

7. **Update the Project**

   To install dependencies and apply migrations in one step (e.g., after pulling new changes):

   .. code-block:: bash

      make update

   This command combines `make install` and `make migrate`.

Additional Notes
----------------

- Ensure you have an active virtual environment managed by Poetry. The Makefile commands use `poetry run` to execute commands within the virtual environment.
