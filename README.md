# Project Setup Guide
To improve medical center operations, **JUMCMS (Jahangirnagar University Medical Center Management System)** is a web application built with Django. For Admins, Doctors, Patients, Lab technicians, and Store managers, it provides functionality tailored to their roles. Prescription management, test reporting, inventory control, and appointment scheduling are all made easier by the system. This guide will help you set up and run the project.

## Prerequisites
- Python 3.12.4 installed

## Setup

1. Check the existence of Python and pip:
    - For Windows:
    
        ```sh
        python --version
        pip --version
        ```

    - For macOS/Linux:
    
        ```sh
        python3 --version
        pip3 --version
        ```

2. Create a virtual environment in a particular directory:
    - For Windows:
    
        ```sh
        python -m venv myenv
        ```
    - For macOS/Linux:
    
        ```sh
        python3 -m venv myenv
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

4. Clone the repository:<br>
   **Using Https:**

    ```bash
    git clone https://github.com/SubarnaSaha08/JUMCMS-Jahangirnagar-University-Medical-Center-Management-System.git
    cd JUMCMS-Jahangirnagar-University-Medical-Center-Management-System
    ```
    **Using SSH:**

    ```bash
    git clone git@github.com:SubarnaSaha08/JUMCMS-Jahangirnagar-University-Medical-Center-Management-System.git
    cd JUMCMS-Jahangirnagar-University-Medical-Center-Management-System
    ```

5. Install the required packages from `requirements.txt`:

    - For Windows:
    
        ```bash
        pip install -r requirements.txt
        ```
    - For macOS/Linux:
    
        ```bash
        pip3 install -r requirements.txt
        ```


6. Enter to the Django project repository:

    ```bash
    cd jumcms
    ```

### VSCode Configuration

1. Install the **Python** extension in VSCode.

2. Select the Python interpreter for the virtual environment:
    - Open Command Palette (View -> Command Palette).
    - Select `Python: Select Interpreter`.
    - Enter the path to the interpreter: `myenv/Scripts/python.exe`.

3. Install **SQLite** Viewer to view the database file.

### Database Setup

1. Create database migrations:
	- For Windows:
	
   		 ```bash
   		 python manage.py makemigrations
   		 ```
	- For macOS/Linux:
	
		```bash
		python3 manage.py makemigrations
    	```

2. Apply the migrations:
 	- For Windows:

    	```bash
    	python manage.py migrate
    	```
 	- For macOS/Linux:
 	
		```bash
		python3 manage.py migrate
		```

### Running the Server

1. Start the Django development server:
	- For Windos:
	
	 	```bash
    	python manage.py runserver
    	```
	- For macOs/Linux:
	
		```bash
    	python3 manage.py runserver
    	```