import os
import helpers
import jinja2
import sys, setuptools, tokenize

from helpers import usd, datetimeformat
from flask import Flask, render_template, config
from flask_sqlalchemy import SQLAlchemy
from flask_assets import Environment, Bundle

from sassutils.wsgi import SassMiddleware



app = Flask(__name__)

app.config.from_pyfile('settings.py')


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

##where to find the database and initialize SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Barkley.915@127.0.0.1/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) 

##option to tell SQLALchemy that we’re way too lazy to do that, and for every model it should just 
#look at the columns that already exist in the table. This is called reflecting
db.Model.metadata.reflect(db.engine)

class Congress(db.Model):
    __tablename__ = 'sen'
    __table_args__ = { 'extend_existing': True }
    id = db.Column(db.Text, primary_key=True) 


## access sass
app.wsgi_app = SassMiddleware(app.wsgi_app, {
    'app': ('static/assets/sass', 'app/static/assets/css/light-bootstrap-dashboard.css', 'app/static/assets/css/light-bootstrap-dashboard.css')
})

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

from app import routes
