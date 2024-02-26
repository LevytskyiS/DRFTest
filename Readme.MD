Django REST Framework Application

How to Run:

1. Download the archive or clone this repository:

git clone 'https://github.com/LevytskyiS/DRFTest.git'

2. Install and activate a virtual environment:

Create a virtual environment
'python -m venv venv'

Activate the virtual environment
'.venv/Scripts/activate'

3. Navigate to the project folder (cd drfsite) and install the requirements by running:

'pip install -r requirements.txt'

4. Run the PostgreSQL Docker container:

'docker-compose up -d'

5. Apply migrations for the project if needed:

'python manage.py migrate'

6. Run the Django server:

'python manage.py runserver'