import os
from os import environ 

DATABASE_URL = environ.get('DATABASE_URL')
# SECRET_KEY = os.urandom(24)
API_KEY = environ.get('API_KEY')


