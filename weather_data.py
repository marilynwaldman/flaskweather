# Program wxwarning
# by Todd Arbetter (todd.e.arbetter@gmail.com)
# Software Engineer, IXMap, Golden, CO

# collects latests National Weather Service Warnings, Watches, Advisories,
# and Statements, plots shapefiles on an interactive map in various colors.
# The map is able to pan and zoom, and on mouseover will give the type of
# weather statement, start, and expiry.


import time
import tarfile
import os as os
import urllib3
import shutil
#from pathlib import Path
import geopandas as gpd
import pandas as pd
import datetime as dt

def open_tarfile(destination):
    try:
        f = tarfile.open(destination)
    except:
        return None  
    return f          

def awaitdata(destination, dest_path):
    for i in range (0,10):
         #if  os.path.exists(destination, dest_path): 
        print("*****in await*****")
        if tarfile.is_tarfile(destination): 
            f = open_tarfile(destination)
            if f is not None:
                f.extractall(path=str(dest_path)+'/current_all/')
                return True

    time.sleep(1)
    return False


def get_weather_data(app):
    # We create a downloads directory within the streamlit static asset directory
    # and we write output files to it

    #get latest wx warnings from NWS

    url='https://tgftp.nws.noaa.gov/SL.us008001/DF.sha/DC.cap/DS.WWA/current_all.tar.gz'
     
    timestamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')
    
    dest_path = os.path.join(os.getcwd(), 'downloads/')
    dest_path = os.path.join(dest_path, timestamp + '/')
    os.mkdir(dest_path)
     
      
    destination =  str(dest_path)+'current_all.tar.gz'

    http = urllib3.PoolManager()
    try:
        resp = http.request(
            "GET",
            url,
            preload_content=False)
        with open(destination,"wb") as f:
            for chunk in resp.stream(32):
                f.write(chunk)

        resp.release_conn() 
        """
        wxdata = awaitdata(destination, dest_path)
        if not wxdata:
            return None, timestamp
        """
    except Exception as e:
        return None, timestamp


    wxdata = awaitdata(destination, dest_path)
    if not wxdata:
        return None, timestamp
    """
    try:
        print("in extract")
        wxdata.list(verbose=True)
        wxdata.extractall(path=str(dest_path)+'/current_all/')
    except Exception as e:
            print(dest_path)
            return None 
    """
    infile = str(dest_path) + '/current_all/current_all.shp'
         
    if os.path.exists(infile):
            print("in geopandas")
            weather_df = gpd.read_file(infile)    
            weather_df = weather_df.drop(columns=['PHENOM','SIG','WFO','EVENT','CAP_ID','MSG_TYPE','VTEC'])  
            print(dest_path)
            shutil.rmtree(dest_path)
            return weather_df, timestamp
    else:
            return None, timestamp     



  



