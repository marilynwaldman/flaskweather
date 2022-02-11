# Program wxwarning
# by Todd Arbetter (todd.e.arbetter@gmail.com)
# Software Engineer, IXMap, Golden, CO

# collects latests National Weather Service Warnings, Watches, Advisories,
# and Statements, plots shapefiles on an interactive map in various colors.
# The map is able to pan and zoom, and on mouseover will give the type of
# weather statement, start, and expiry.


import os as os
from functools import wraps, update_wrapper
from datetime import datetime
#from pathlib import Path
from weather_data import  get_weather_data
from weather_map import make_weather_map 
import geopandas as gpd
import pandas as pd
import shutil
import datetime as dt



#from ediblepickle import checkpoint
from flask import Flask, render_template, render_template_string, request, redirect, url_for, send_file, make_response

# Define global environoment:
#  1.  Paths to maps and images such as the logo
#  2.  Create directories for maps to be created.  First delete old
#      directories if they exist.

dest_path = os.path.join(os.getcwd(), 'downloads/')
     
if not os.path.exists(dest_path):
         os.mkdir(dest_path) 
         print("made downloads director")


server = Flask(__name__)

#Bootstrap(app)
server.config['TEMPLATES_AUTO_RELOAD'] = True
server.vars = {}
cwd = os.getcwd()

logo_path = os.path.join(cwd, 'static/img/logo.png' )
server.vars['logo_path'] = logo_path

#server.vars['map_html'] = None

# Set up cache headers and directives
def nocache(view):
  @wraps(view)
  def no_cache(*args, **kwargs):
    response = make_response(view(*args, **kwargs))
    response.headers['Last-Modified'] = datetime.now()
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response
        
  return update_wrapper(no_cache, view)

# Define the "root" route.   Redirect to index

@server.route('/')
@nocache
def main():
  return redirect('/index.html')

#  Define the index route: GET 

@server.route('/index.html', methods=['GET'])
@nocache
def index():
  if request.method == 'GET':
    
  
    #map_html =  server.vars.get("map_html")

    # Get weather data (geopandas dataframe)
    weather_df, timestamp =  get_weather_data(server)

    if weather_df is None:
      return redirect('/dataerror.html')

    # Create the map

    map_html = make_weather_map(weather_df)
    if map_html is None:
      print("map not saved")
      return redirect('/maperror.html')
    server.vars['map_html'] = map_html  
    # get the current time in UTC (constant reference timezone)
    
    server.vars['Title_line1'] = 'Current U.S. Weather Statements'
    #timestamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec='minutes')
    #print(timestamp)
    server.vars['Title_line2'] = timestamp[0:10]+' '+timestamp[11:16]+' UTC'
    return render_template('display.html', vars=server.vars)



@server.route('/maps/map.html')
@nocache
def show_map():
  print("show map")
  return render_template_string(server.vars['map_html'])
  


@server.route('/get_logo')
def get_logo():
  #print("in get logo")
  #logo_path = os.path.join(server.root_path, 'static/img/logo.png' )
  logo_path = server.vars.get("logo_path")
  #logo_file = Path(logo_path)
  #print(logo_path)
  if os.path.exists(logo_path):
    #print("logo found")
    return send_file(logo_path)
  else:
    return render_template('error.html', culprit='logo file', details="the logo file couldn't be loaded")

  pass


@server.route('/error.html')
def error():
  details = "There was some kind of error."
  return render_template('error.html', culprit='logic', details=details)

@server.route('/apierror.html')
def apierror():
  details = "There was an error with one of the API calls you attempted."
  return render_template('error.html', culprit='API', details=details)

@server.route('/maperror.html')
def maperror():
  details = "Map not found."
  return render_template('error.html', culprit='the Map', details=details)

@server.route('/dataerror.html')
def dataerror():
  details = "Weather data not found or took took much time to load."
  return render_template('error.html', culprit='the Weather Data', details=details)
