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
from helpers import extract_values, bar, candSummary, pie 
from flask import render_template, request, request, jsonify, redirect, flash
from bokeh.embed import components

@app.route('/', methods=["GET","POST"])
def index():
    if request.method =='GET':
        
        return render_template("index.html")

    else:
        
        return redirect("/candidate")
        

@app.route("/candidate", methods=["GET", "POST"])
def candidate():
    if request.method == "POST":
        """ build candidate page """
        ##extract from SQLAlchemy query
        fullname = request.form.get("autobutton").split(" ", 1)
        search = Congress.query.filter_by(first_name = fullname[0],
                                       last_name = fullname[1]).first()
        
        ##parse data that cant be displayed by jinja
        if search.party == "D":
            search.party = "Democrat"
        elif search.party == "R":
            search.party = "Republican"
        else: 
            search.party = "Independent"

        ### get picture from github
        picurl = (f'https://theunitedstates.io/images/congress/225x275/{search.id}.jpg')
        
        """CRP lib to pull from open secrets api"""
        crp = CRP()
        rows = crp.candidates.contrib(search.crp_id)
        sectors = crp.candidates.sector(search.crp_id)
        
        """bokeh functions to create plots"""
        gscript, gdiv = bar(rows)
        pscript, pdiv = pie(sectors)

        ### return summary data for cards
        cards = candSummary(search.crp_id)
        
        return  render_template("candidate.html", picurl = picurl,  search = search, rows = rows, sectors = sectors, cards = cards, 
                                gscript = gscript, gdiv= gdiv, pscript = pscript, pdiv = pdiv)









