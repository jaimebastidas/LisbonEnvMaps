from fileinput import filename
from turtle import width
import etl as e
import argparse
import time
import sys
import pandas as pd
import numpy as np
import plotly.express as px
import geopandas as gpd
import datetime
from osgeo import gdal



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

        print(query_df.head())

        # print(query_df.shape)
        
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
    
    #print(geo_hum.iloc[:,-1])
    #print(geo_temp.head())
    #print(geo_noise.head())
    #print(geo_hum.head())

    list_geogdf = [geo_temp, geo_noise, geo_hum]

    return list_geogdf

def plot_maps(list_geo):

    print("the list is:")
    #print(list_geo)

    

# = world.to_crs("EPSG:3395") # world.to_crs(epsg=3395) would also work

#ax = world.plot()

#ax.set_title("Mercator");
    
    i = 0
    for m in list_geo:

        #m = m.to_crs("EPSG:27429")



        i = i+1 
        filename = (str(i) + '.tif')

        

        zvalue = m.columns[-1]

        bounds = m.total_bounds
        #bounds =  [491852.55724386,
        #                        4293589.0484153,
        #                       481739.61788112,
        #                       4284064.37306832]

        print(bounds)

        pixel_size = 10

        width = round((bounds[2] - bounds[0])/pixel_size)
        height = round((bounds[3] - bounds[1])/pixel_size)

        #opt = gdal.GridOptions(format="GTiff", width=width, height=height, outputBounds=bounds, outputSRS="EPSG:27429", algorithm="invdist", zfield=zvalue)

        input = gdal.OpenEx(m.to_json(), gdal.OF_VECTOR)
       

        #IDW_gdal = gdal.Grid(f"{PLOTS}/{filename}", input ,outputSRS = "EPSG:27429", zfield = zvalue, algorithm = "invdist", outputBounds = bounds, width = 20, height = 20)

        #IDW_gdal = gdal.Grid(f"{PLOTS}/{filename}", input, zfield = zvalue, algorithm = "invdist", outputBounds = bounds, width = 20, height = 20)
        
        IDW_gdal = gdal.Grid(f"{TEMP}/{filename}", input, format="GTiff", width=width, height=height, outputBounds=bounds, algorithm="invdist", zfield=zvalue)

        #IDW_gdal_reproyected = 

        #outputBounds = [ulx, uly,   lrx,        lry],

        # ds = gdal.Grid('result.tif', 'points.shp', format='GTiff',
        #        outputBounds=[0.0, 0.0, 100.0, 100.0],
        #        width=10, height=10, outputType=gdal.GDT_Float32,
        #        algorithm='invdist:power=2.0:smoothing=1.0',
        #        zfield='height'

        # gdal.OpenEx(df_new.to_json(), gdal.OF_VECTOR)

        # Output_dataset_name = "D:xxxxxxxinvdist.tif"
        # input_shape_file_name = r'D:xxxxxxxnearest.shp'

        
        # raster_width = 250.0
        # raster_height = 250.0

        # IDW_gdal = gdal.Grid(Output_dataset_name, input_shape_file_name, zfield="rs",
        #        algorithm = "invdist", 
        #        ,
        #       width = raster_width, height = raster_height)
        
        # outputBounds = [491852.55724386,
        #                         4293589.0484153,
        #                         481739.61788112,
        #                         4284064.37306832]
        
        # print(filename)
    
        # fig = px.choropleth(m, geojson=m.geometry,locations=m.index,color="id_sensor")

        # fig.update_geos(fitbounds="locations", visible=False)
 
        # fig.write_image(f"{PLOTS}/{filename}", engine='kaleido')



def parse_args() -> str:
    """ Reads command line arguments

        Returns:
            the name of the configuration file
    """
    parser = argparse.ArgumentParser(description="GPS: project")
    parser.add_argument("--config_file", required=False, help="The configuration file",default="./config/00.yml")
    args = parser.parse_args()
    return args.config_file


def main(config_file: str) -> None:

    """Main function for Query data and creating maps

    Args:
        config_file (str): configuration file
    """

    parser = argparse.ArgumentParser(description='Enviromental Maps for Lisbon')
    parser.add_argument('--initial_date', type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'), help="indicate the initial date, e.g.:2022-02-20")       
    parser.add_argument('--final_date', type=lambda s: datetime.datetime.strptime(s, '%Y-%m-%d'), help="indicate the final date, e.g.:2022-02-20")

    #parser.add_argument('--initial_date', type=str, help="indicate the initial date, e.g.:2022-02-20")
    #parser.add_argument('--final_date', type=str, help="indicate the final date, e.g.:2022-02-22")
    
    args = parser.parse_args()

    initial_date = "'2022-02-12'" if not args.initial_date else args.initial_date
    final_date = "'2022-02-14'" if not args.final_date else args.final_date

    
    config = e.read_config(config_file)
    

    e.info("EXECUTING QUERY FOR SELECTED DATES")

    filtered_df = querydata(config, initial_date, final_date)

    e.info("SUMMARIZING ENV VARIABLES FOR MAPS")

    list_geo = sum_variables(config, filtered_df)

    plot_maps(list_geo)


if __name__ == "__main__":
    config_file = parse_args()
    main(config_file)
