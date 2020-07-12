import os
from os import environ 


DATABASE_URL = environ.get('DATABASE_URL')
SECRET_KEY = environ.get('SECRET_KEY')
API_KEY = environ.get('API_KEY')


