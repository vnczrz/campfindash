import os
import requests
import json
from datetime import date
import urllib.parse
import crpapi
import pandas as pd

from math import pi
from crpapi import CRP
from flask import redirect, render_template, request, jsonify
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from bokeh.models import ColumnDataSource, Legend
from bokeh.plotting import figure, output_file, show
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.palettes import Category20c
from bokeh.transform import cumsum

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

def candSummary(CRPid):
    """pull cand summary from API for top cards"""
    #create client
    crp = CRP()
    #contact API
    data = crp.candidates.summary(CRPid)
    
    ###parse response adn return dictionar
    try:
        return {
            "total": data['total'],
            "spent": data['spent'],
            "on_hand": data['cash_on_hand'],
            "cycle": data["cycle"],
            "source": data["source"],
            "last_updated": data["last_updated"],
            "origin": data["origin"]
        }
    except (KeyError, TypeError, ValueError):
        return None  

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


####Created postgresql-encircled-34732 as DATABASE_URL












    



