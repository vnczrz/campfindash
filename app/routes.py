import os
import requests
import json
import sqlite3
import datetime
import crpapi
import jinja2

from crpapi import CRP
from flask_sqlalchemy import SQLAlchemy
from app import app, Congress
from helpers import extract_values, bar, candSummary, pie, buildSesh 
from flask import render_template, request, request, jsonify, redirect, flash, session
from bokeh.embed import components

@app.route('/', methods=["GET","POST"])
def index():
    if request.method =='GET':
        session.clear()
        return render_template("index.html")

    else:
        """build session var"""
        ##extract from SQLAlchemy query
        fullname = request.form.get("autobutton").split(" ", 1)
        search = Congress.query.filter_by(first_name = fullname[0],
                                       last_name = fullname[1]).first()
        buildSesh(search)
        
        ### return summary data for cards
        candSummary(session["crp_id"])
        
        return render_template("layout.html")
        
@app.route("/sector", methods=['GET'])
def sector():
    """CRP lib to pull from open secrets api"""
    crp = CRP()

    """create plots"""    
    sectors = crp.candidates.sector(session["crp_id"])
    pscript, pdiv = pie(sectors)

    return render_template("sector.html", sectors = sectors, pscript = pscript, pdiv = pdiv)

@app.route("/contribs", methods=['GET'])
def contribs():
    """CRP lib to pull from open secrets api"""
    crp = CRP()

    """create plots"""
    rows = crp.candidates.contrib(session["crp_id"])
    gscript, gdiv = bar(rows)

    return render_template("contribs.html", rows =rows, gscript = gscript, gdiv= gdiv)








