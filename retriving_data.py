from asyncio import constants
from fiona import bounds
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
from matplotlib import cm, pyplot
import pathlib
#import contextily as cx
from create_report import content_report

# constant values

STATIC_DIR = "data/static"
PLOTS = "data/plots"
TEMP = "data/tifs"



#def querydata(config: dict, initial_date: str, final_date: str) -> pd.DataFrame:
def querydata(config: dict, initial_date: str, final_date: str) -> list:

    query = f'''select id_sensor, avg(temp_value) as temp,  avg(noise_value) as noise, avg(hum_value) as humidity 
                from us.env_variables 
                where date >= {initial_date} and date <= {final_date}
                group by id_sensor'''
    
    query_ts = f'''select date, avg(temp_value) as temp,  avg(noise_value) as noise, avg(hum_value) as humidity 
                from us.env_variables 
                where date >= {initial_date} and date <= {final_date}
                group by date'''
    
    try:
        connection = e.DBController(**config["database"])
        
        query_df = connection.select_data(query)

        query_ts_df = connection.select_data(query_ts)

        #print(query_df.head())

        list_querys_df = [query_df, query_ts_df]

        if (query_df.shape[0] or query_ts_df.shape[0]) == 0:

            e.done("CHOOSE OTHER DATES INTERVAL, THERE ARE NOT DATA FOR YOUR DATES")    
        
    except Exception as err:
        
        e.die(f"error in query data: {e}")
    
    #return query_df, query_ts_df
    return list_querys_df

#def sum_variables(config: dict, filtered_df:pd.DataFrame) -> list:
def sum_variables(config: dict, filtered_df_list) -> list:

    filtered_df = filtered_df_list[0]
    filtered_df_ts = filtered_df_list[1]

    #print(filtered_df)
    print(filtered_df_ts)
    #print(filtered_df_ts.dtypes)

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

    return list_geogdf, filtered_df_ts

def interpolation(list_geo):

    #constants for this function
    i = 0
    bounds = [-9.24, 38.8, -9.08, 38.68]


    for m in list_geo:

        i = i+1
        filename = (str(i) + '.tif')
        file = pathlib.Path(f"{TEMP}/{filename}")
        if file.exists():
            os.remove(file) 
    
        zvalue = m.columns[-1]

    # operation for setting pixel size close to 10 meters


        pixel_size = 10

        width = round((bounds[2] - bounds[0])/pixel_size)
        height = round((bounds[3] - bounds[1])/pixel_size)

        #opt = gdal.GridOptions(format="GTiff", width=width, height=height, outputBounds=bounds, outputSRS="EPSG:27429", algorithm="invdist", zfield=zvalue)
    # convert the deodataframe and IDW operation for interpolation
        input = gdal.OpenEx(m.to_json(), gdal.OF_VECTOR)
        
        IDW_gdal = gdal.Grid(f"{TEMP}/{filename}", input, format="GTiff", width=width, height=height, outputBounds=bounds, algorithm="invdist", zfield=zvalue)


def plots(list_geo, filtered_df_ts:pd.DataFrame):
        

    gdf_lisbon = e.read_geojson(f"{STATIC_DIR}/fraguesias.geojson")

    gdf_lisbon = gdf_lisbon.to_crs(epsg=4326)

    print(gdf_lisbon.total_bounds)


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
     
    fig_t, ax_t = plt.subplots(1, figsize=(8, 5))
    show((r_temp, 1), cmap='viridis', interpolation='none', ax=ax_t)
    show((r_temp, 1), contour=True, ax=ax_t)
    gdf_lisbon.boundary.plot(ax=ax_t, zorder=1, edgecolor='black')
    p_temp.plot(column='temp', ax=ax_t, legend=True, legend_kwds={'label': 'Degrees Celsius', 'orientation': "vertical"}, zorder=2)
    p_temp.plot(ax = ax_t, color = 'black', marker='h', markersize=20, zorder=3)
        #cx.add_basemap(ax)
    ax_t.set_axis_off()
        #plt.show()
    fig_t.savefig(f'{PLOTS}/temperature.png')

        # Noise plot for report

    r_noise = rasterio.open(f"{TEMP}/2.tif")
    p_noise = list_geo[1]
     
    fig_n, ax_n = plt.subplots(1, figsize=(8, 5))
    show((r_noise, 1), cmap='viridis', interpolation='none', ax=ax_n)
    show((r_noise, 1), contour=True, ax=ax_n)
    gdf_lisbon.boundary.plot(ax=ax_n, zorder=1, edgecolor='black')
    p_noise.plot(column='noise', ax=ax_n, legend=True, legend_kwds={'label': 'Decibels', 'orientation': "vertical"}, zorder=2)
    p_noise.plot(ax = ax_n, color = 'black', marker='h', markersize=20, zorder=3)
        #cx.add_basemap(ax)
    ax_n.set_axis_off()
        #plt.show()
    fig_n.savefig(f'{PLOTS}/noise.png')
        
        # Humidity plot for report

    r_hum = rasterio.open(f"{TEMP}/3.tif")
    p_hum = list_geo[2]
     
    fig_h, ax_h = plt.subplots(1, figsize=(8, 5))
    show((r_hum, 1), cmap='viridis', interpolation='none', ax=ax_h)
    show((r_hum, 1), contour=True, ax=ax_h)
    gdf_lisbon.boundary.plot(ax=ax_h, zorder=1, edgecolor='black')
    p_hum.plot(column='humidity', ax=ax_h, legend=True, legend_kwds={'label': 'Humidity Percentage', 'orientation': "vertical"}, zorder=2)
    p_hum.plot(ax = ax_h, color = 'black', marker='h', markersize=20, zorder=3)
        #cx.add_basemap(ax)
    ax_h.set_axis_off()
    
    fig_h.savefig(f'{PLOTS}/humidity.png')

        # average temperature value per date

    filtered_df_ts["date"] = pd.to_datetime(filtered_df_ts["date"])
    
    fig_t_date, ax_td = plt.subplots(figsize=(10, 4))
    filtered_df_ts.groupby(filtered_df_ts['date'].dt.hour)["temp"].plot(kind='bar', rot=0, ax=ax_td)
    plt.xlabel("day");
    plt.ylabel("Lisbon average temperature")

    fig_t_date.savefig(f'{PLOTS}/temp_ts.png')

        # average noise value per date

    filtered_df_ts["date"] = pd.to_datetime(filtered_df_ts["date"])

    fig_n_date, ax_nd = plt.subplots(figsize=(10, 4))
    filtered_df_ts.groupby(filtered_df_ts['date'].dt.hour)["noise"].plot(kind='bar', rot=0, ax=ax_nd)
    plt.xlabel("day");
    plt.ylabel("Lisbon average noise")

    fig_n_date.savefig(f'{PLOTS}/noise_ts.png')

        # average humidity value per date
    filtered_df_ts["date"] = pd.to_datetime(filtered_df_ts["date"])

    fig_h_date, ax_hd = plt.subplots(figsize=(10, 4))
    filtered_df_ts.groupby(filtered_df_ts['date'].dt.hour)["humidity"].plot(kind='bar', rot=0, ax=ax_hd)
    plt.xlabel("day");
    plt.ylabel("Lisbon average temperature")

    fig_h_date.savefig(f'{PLOTS}/hum_ts.png')


# def parse_args() -> str:
#     """ Reads command line arguments

#         Returns:
#             the name of the configuration file
#     """
#     parser = argparse.ArgumentParser(description='Enviromental Maps for Lisbon')
#     parser.add_argument("--config_file", required=False, help="The configuration file",default="./config/00.yml")
#     parser.add_argument('--initial_date',required=False, type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'), help="indicate the initial date, e.g.:2022-02-20", default="2022-02-12")       
#     parser.add_argument('--final_date',required=False, type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'), help="indicate the final date, e.g.:2022-02-20", default="2022-02-19")

#     args = parser.parse_args()

#     #initial_date = "'2022-02-12'" if not args.initial_date else args.initial_date
#     #final_date = "'2022-02-19'" if not args.final_date else args.final_date

    
#     return args.config_file, args.initial_date, args.final_date
    #return args.config_file


def main(config_file: str, initial_date:str, final_date:str) -> None:

    """Main function for Query data and creating maps

    Args:
        config_file (str): configuration file
        initial_date (str): the initial date for querying data using this format: yyyy-mm-dd
        final_date (str): the final date for querying data using this format: yyyy-mm-dd
    """
    
    config = e.read_config(config_file)
    

    e.info("EXECUTING QUERY FOR SELECTED DATES")

    #filtered_df = querydata(config, initial_date, final_date)
    filtered_df_list = querydata(config, initial_date, final_date)

    e.info("SUMMARIZING ENV VARIABLES FOR MAPS")

    #list_geo = sum_variables(config, filtered_df)
    list_geo, filtered_df_ts = sum_variables(config, filtered_df_list)

    e.info("CREATING RASTER FILES OF INTERPOLATION")

    interpolation(list_geo)

    e.info("PLOTING ENV VARIABLE MAPS")

    plots(list_geo, filtered_df_ts)

    e.info("CREATING PDF FILE")

    pdfname = config["fname_report"]

    content_report(pdfname, initial_date, final_date)


if __name__ == "__main__":

    #config_file = parse_args()
    #config_file = parse_args(['--config_file'])
    #initial_date = parse_args(['--initial_date'])
    #final_date = parse_args(['--final_date'])
    
    #main(config_file, initial_date, final_date)
    #main(config_file)

    parser = argparse.ArgumentParser(description='Enviromental Maps for Lisbon')
    parser.add_argument("--config_file", required=False, help="The configuration file",default="./config/00.yml")
    parser.add_argument('--initial_date',required=False, type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'), help="indicate the initial date, e.g.:2022-02-20")       
    parser.add_argument('--final_date',required=False, type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'), help="indicate the final date, e.g.:2022-02-20")
    
    
    args = parser.parse_args()
    
    config_file = "./config/00.yml" if not args.config_file else args.config_file
    initial_date = "'2022-02-01'" if not args.initial_date else args.initial_date
    final_date = "'2022-02-20'" if not args.final_date else args.final_date

    main(config_file, initial_date, final_date)
