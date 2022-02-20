import etl as e
import argparse
import time
import os, sys
import pandas as pd
import numpy as np
import plotly.express as px
import geopandas as gpd
import datetime
from osgeo import gdal
import rasterio
import matplotlib.pyplot as plt
from rasterio.plot import show
from matplotlib import pyplot
import pathlib
#import contextily as cx
from create_report import content_report

# constant values

STATIC_DIR = "data/static"
PLOTS = "data/plots"
TEMP = "data/tifs"



def querydata(config: dict, initial_date: str, final_date: str) -> pd.DataFrame:

    query = f'''select id_sensor, avg(temp_value) as temp,  avg(noise_value) as noise, avg(hum_value) as humidity 
                from us.env_variables 
                where date >= {initial_date} and date <= {final_date}
                group by id_sensor'''
    
    try:
        connection = e.DBController(**config["database"])
        
        query_df = connection.select_data(query)

        #print(query_df.head())

        if query_df.shape[0] == 0:

            e.done("CHOOSE OTHER DATES INTERVAL, THERE ARE NOT DATA FOR YOUR DATES")    
        
    except Exception as err:
        
        e.die(f"error in query data: {e}")
    
    return query_df

def sum_variables(config: dict, filtered_df:pd.DataFrame) -> list:

    temp = filtered_df[['id_sensor','temp']].dropna()

    noise = filtered_df[['id_sensor','noise']].dropna()

    humidity = filtered_df[['id_sensor','humidity']].dropna()

# creating geodaframes

    sensors = config["fname_stations"]
    gdf_sensors = e.read_geojson(f"{STATIC_DIR}/{sensors}")

    gdf_sensors = gdf_sensors.to_crs(epsg=4326)
        
    geo_temp = gdf_sensors.merge(temp, on = 'id_sensor')
  
    geo_temp = geo_temp[['id_sensor', 'lat', 'long', 'geometry', 'temp']]

    geo_noise = gdf_sensors.merge(noise, on = 'id_sensor')
    
    geo_noise = geo_noise[['id_sensor', 'lat', 'long', 'geometry', 'noise']]

    geo_hum = gdf_sensors.merge(humidity, on = 'id_sensor')
    
    geo_hum = geo_hum[['id_sensor', 'lat', 'long', 'geometry', 'humidity']]

    list_geogdf = [geo_temp, geo_noise, geo_hum]

    return list_geogdf

def interpolation(list_geo):
    
    i = 0
    for m in list_geo:

        #m = m.to_crs("EPSG:27429")

        i = i+1
        filename = (str(i) + '.tif')
        file = pathlib.Path(f"{TEMP}/{filename}")
        if file.exists():
            os.remove(file) 
    
        zvalue = m.columns[-1]

        bounds = m.total_bounds
        #print(bounds)

        pixel_size = 10

        width = round((bounds[2] - bounds[0])/pixel_size)
        height = round((bounds[3] - bounds[1])/pixel_size)

        #opt = gdal.GridOptions(format="GTiff", width=width, height=height, outputBounds=bounds, outputSRS="EPSG:27429", algorithm="invdist", zfield=zvalue)

        input = gdal.OpenEx(m.to_json(), gdal.OF_VECTOR)
        
        IDW_gdal = gdal.Grid(f"{TEMP}/{filename}", input, format="GTiff", width=width, height=height, outputBounds=bounds, algorithm="invdist", zfield=zvalue)


def plots(list_geo):
        
    
    if len(os.listdir(PLOTS)) > 0:
        
        for f in os.listdir(PLOTS):

            file_path = os.path.join(PLOTS, f)
            try:
                os.remove(file_path)
            except:
                pass
    
        # Temperature plot for report

    r_temp = rasterio.open(f"{TEMP}/1.tif")
    p_temp = list_geo[0]
     
    fig_t, ax_t = plt.subplots(1, figsize=(15, 12))
    show((r_temp, 1), cmap='viridis', interpolation='none', ax=ax_t)
    show((r_temp, 1), contour=True, ax=ax_t)
    p_temp.plot(column='temp', ax=ax_t, legend=True, legend_kwds={'label': 'Degrees Celsius', 'orientation': "vertical"}, zorder=1)
    p_temp.plot(ax = ax_t, color = 'black', marker='h', markersize=20, zorder=2)
        #cx.add_basemap(ax)
    ax_t.set_axis_off()
        #plt.show()
    fig_t.savefig(f'{PLOTS}/temperature.png')

        # Noise plot for report

    r_noise = rasterio.open(f"{TEMP}/2.tif")
    p_noise = list_geo[1]
     
    fig_n, ax_n = plt.subplots(1, figsize=(15, 12))
    show((r_noise, 1), cmap='viridis', interpolation='none', ax=ax_n)
    show((r_noise, 1), contour=True, ax=ax_n)
    p_noise.plot(column='noise', ax=ax_n, legend=True, legend_kwds={'label': 'Decibels', 'orientation': "vertical"}, zorder=1)
    p_noise.plot(ax = ax_n, color = 'black', marker='h', markersize=20, zorder=2)
        #cx.add_basemap(ax)
    ax_n.set_axis_off()
        #plt.show()
    fig_n.savefig(f'{PLOTS}/noise.png')
        
        # Humidity plot for report

    r_hum = rasterio.open(f"{TEMP}/3.tif")
    p_hum = list_geo[2]
     
    fig_h, ax_h = plt.subplots(1, figsize=(15, 12))
    show((r_hum, 1), cmap='viridis', interpolation='none', ax=ax_h)
    show((r_hum, 1), contour=True, ax=ax_h)
    p_hum.plot(column='humidity', ax=ax_h, legend=True, legend_kwds={'label': 'Humidity Percentage', 'orientation': "vertical"}, zorder=1)
    p_hum.plot(ax = ax_h, color = 'black', marker='h', markersize=20, zorder=2)
        #cx.add_basemap(ax)
    ax_h.set_axis_off()
    
    fig_h.savefig(f'{PLOTS}/humidity.png')

    
        # fig = px.choropleth(m, geojson=m.geometry,locations=m.index,color="id_sensor")
        # fig.update_geos(fitbounds="locations", visible=False)
        # fig.write_image(f"{PLOTS}/{filename}", engine='kaleido')

def parse_args() -> str:
    """ Reads command line arguments

        Returns:
            the name of the configuration file
    """
    parser = argparse.ArgumentParser(description='Enviromental Maps for Lisbon')
    parser.add_argument("--config_file", required=False, help="The configuration file",default="./config/00.yml")
    parser.add_argument('--initial_date',required=False, type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'), help="indicate the initial date, e.g.:2022-02-20", default="2022-02-12")       
    parser.add_argument('--final_date',required=False, type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'), help="indicate the final date, e.g.:2022-02-20", default="2022-02-19")

    args = parser.parse_args()

    #initial_date = "'2022-02-12'" if not args.initial_date else args.initial_date
    #final_date = "'2022-02-19'" if not args.final_date else args.final_date

    
    return args.config_file, args.initial_date, args.final_date


def main(config_file: str, initial_date:str, final_date:str) -> None:

    """Main function for Query data and creating maps

    Args:
        config_file (str): configuration file
    """

    #parser = argparse.ArgumentParser(description='Enviromental Maps for Lisbon')
    #parser.add_argument('--initial_date',required=False, type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'), help="indicate the initial date, e.g.:2022-02-20")       
    #parser.add_argument('--final_date',required=False, type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'), help="indicate the final date, e.g.:2022-02-20")
    
    
    #args = parser.parse_args()

    #initial_date = "'2022-02-12'" if not args.initial_date else args.initial_date
    #final_date = "'2022-02-19'" if not args.final_date else args.final_date

    
    config = e.read_config(config_file)
    

    e.info("EXECUTING QUERY FOR SELECTED DATES")

    filtered_df = querydata(config, initial_date, final_date)

    e.info("SUMMARIZING ENV VARIABLES FOR MAPS")

    list_geo = sum_variables(config, filtered_df)

    e.info("CREATING RASTER FILES OF INTERPOLATION")

    interpolation(list_geo)

    e.info("PLOTING ENV VARIABLE MAPS")

    plots(list_geo)

    e.info("CREATING PDF FILE")

    content_report(config_file, initial_date, final_date)


if __name__ == "__main__":

    config_file = parse_args()
    initial_date = parse_args()
    final_date = parse_args()
    
    main(config_file, initial_date, final_date)
