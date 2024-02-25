Django REST Framework Application

How to run:

1. Download the archive or clone this repository: git clone 'https://github.com/LevytskyiS/DRFTest.git'

2. Install and activate a virtual environment: 
2.1. python -m venv venv 
2.2. ./venv/Scripts/activate

3. Move to the project folder (cd drfsite) and install the requirements by runnning the 'pip install -r requirements.txt' command.

4. Run PostgreSQL docker container by running the 'docker-compose up -d' command.

5. Apply migrations for the project if needed: 
'python manage.py migrate'
'python manage.py migrate eshop'

6. Run server - 'python manage.py runserver'