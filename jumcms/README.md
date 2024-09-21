# Project Setup Guide
This guide will help you set up and run the project.

## Prerequisites
- Python 3.12.4 installed

## Setup

1. Check the existence of Python and pip:

    ```sh
    python --version
    pip --version
    ```

2. Create a virtual environment:

    ```sh
    python -m venv myenv
    ```

3. Activate the virtual environment:

    - For Windows:

        ```sh
        .\myenv\Scripts\activate
        ```

    - For macOS/Linux:

        ```sh
        source myenv/bin/activate
        ```

4. Install the required packages from `requirements.txt`:

    ```sh
    pip install -r requirements.txt
    ```

### VSCode Configuration

1. Install the Python extension in VSCode.

2. Select the Python interpreter for the virtual environment:
    - Open Command Palette (View -> Command Palette).
    - Select `Python: Select Interpreter`.
    - Enter the path to the interpreter: `myenv/Scripts/python.exe`.

3. Install SQLite Viewer to view the database file.

### Database Setup

1. Create database migrations:

    ```sh
    python manage.py makemigrations
    ```

2. Apply the migrations:

    ```sh
    python manage.py migrate
    ```

### Running the Server

1. Start the Django development server:

    ```sh
    python manage.py runserver
    ```

### Creating a New Django Project

To create a new Django project, use the following command:

```sh
django-admin startproject project_name
```
