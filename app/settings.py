import os
from os import environ 




# SQLALCHEMY_DATABASE_URI = os.environ.get('sqlite:///congress.sqlite3')
SECRET_KEY = environ.get('SECRET_KEY')
API_KEY = environ.get('API_KEY')

##where to find the database and initialize SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')