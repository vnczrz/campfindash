import os
from os import environ 

DATABASE_URL = 'postgresql://postgres:Barkley.915@127.0.0.1/postgres'
# SQLALCHEMY_DATABASE_URI = os.environ.get('sqlite:///congress.sqlite3')
SECRET_KEY = environ.get('SECRET_KEY')
API_KEY = environ.get('API_KEY')