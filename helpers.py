import os
import requests
import json
from datetime import date
import urllib.parse
import crpapi
import pandas as pd

from functools import wraps
from math import pi
from crpapi import CRP
from flask import redirect, render_template, request, jsonify, session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from bokeh.models import ColumnDataSource, Legend
from bokeh.plotting import figure, output_file, show
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.palettes import Category20c
from bokeh.transform import cumsum


def login_required(f):
    """Decorate routes to require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("crp_id") is None:
            return redirect("/")
        return f(*args, **kwargs)
    return decorated_function

def extract_values(obj, key):
    """Pull all values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return results

def buildSesh(obj):
        """ build candidate navs """
        
        ##parse data that cant be displayed by jinja
        if obj.party == "D":
            obj.party = "Democrat"
        elif obj.party == "R":
            obj.party = "Republican"
        else: 
            obj.party = "Independent"
        
        ###build session
        session["crp_id"] = obj.crp_id
        session["fullname"] = obj.first_name + " " + obj.last_name
        session["title"] = obj.title
        session["state"] = obj.state
        session["DOB"] = obj.date_of_birth
        session["party"] = obj.party
        session["next_election"] = obj.next_election
        session["office"] = obj.office
        session["phone"] = obj.phone
        session["twitter"] = obj.twitter_account
        session["facebook"] = obj.facebook_account
        session["youtube"] = obj.youtube_account
        session["url"] = obj.url
        session["picurl"] = (f'https://theunitedstates.io/images/congress/225x275/{obj.id}.jpg')


def candSummary(CRPid):
    """pull cand summary from API for top cards"""
    #create client
    crp = CRP()
    #contact API
    data = crp.candidates.summary(CRPid)
    
    ###parse response adn return dictionar
    session["total"] = data['total']
    session["spent"] = data['spent']
    session["on_hand"] = data['cash_on_hand']
    session["cycle"] = data["cycle"]
    session["source"] = data["source"]
    session["last_updated"] = data["last_updated"]
    session["origin"] = data["origin"]
  

def bar(obj):
    """pull data from crp api and create bokeh bar plot"""
    #extract data from api request
    org = extract_values(obj, 'org_name')
    ind = extract_values(obj, 'indivs')
    pac = extract_values(obj, 'pacs')
    
    total = ["Individuals", "PAC"]

    data ={'org':org,
           'Individuals':[float(i) for i in ind],
           'PAC':[float(j) for j in pac] }

    #create figure
    p = figure(y_range = org, plot_height = 400, plot_width = 600,
               toolbar_location=None, tools="hover", sizing_mode = 'scale_both')
    #create bar
    p.hbar_stack(total, y = 'org', height = 0.5, color = ["#718dbf", "#e84d60"], source = ColumnDataSource(data), legend_label = total)

    #style graph
    p.hover.tooltips= [("Organization","@org"), 
                        ("Amount",  "$name: $@$name")]
    
    p.legend.orientation = "vertical"
    p.legend.location = "top_right"
    p.xgrid.grid_line_color = None
    p.y_range.range_padding = 0.1
    p.yaxis.visible = False
    p.xaxis[0].formatter.use_scientific = False
    p.x_range.start = 0

    script, div = components(p)
    return script, div

def pie(obj):
    """Pull Data from CRP and plot into Pie"""
    ## clean up data
    sectors = extract_values(obj, "sector_name")
    totals = extract_values(obj, "total")
    totals = [float(i) for i in totals]
    x = dict(zip(sectors, totals))

    ##init data
    data = pd.Series(x).reset_index(name='value').rename(columns={'index':'sector'})
    data['angle'] = data['value']/data['value'].sum() * 2*pi
    data['color'] = Category20c[len(x)]

    ## construct figure
    p = figure(plot_height=325, toolbar_location=None,
            tools="hover", tooltips="@sector: $@value", sizing_mode="scale_both")
    ## construct plot
    p.wedge(x=0, y=1, radius=0.5,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', source=data)

    # p.add_layout(p.legend[0], 'right')

    #style plot
    p.xaxis.visible = False
    p.yaxis.visible = False
    
    script, div = components(p)
    return script, div

def usd(value):
    """Format value as USD."""
    value = float(value)
    return ("${:,.2f}").format(value)

def datetimeformat(value, format='%d-%m-%Y'):
    return value.strftime(format)











    



