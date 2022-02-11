# Weather Map

The weather map is a flask app that reads current weather data from NOAA, creates a folium map and renders the map to the user.

This is a prototype and proof of concept.  In particular evalualte amethods and research for programmatic map making without a gis.  The goal is to assess resource requirements and constraints.


#  This is a flask implementation and will be targeted to aws app runner

# To run locally:

###  Set up local python environment

Have to use conda for geopandas
```
conda create -n geo_env
conda activate geo_env
conda config --env --add channels conda-forge
conda config --env --set channel_priority strict
conda install python=3 geopandas

```

Install geopandas, flask and urllib3 - in anaconada navigator

Build Dockerfile with anaconda


cd  flaskweather
docker build -t flaskweather .
docker run -p 8000:8000 flaskweather 
```
