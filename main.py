import etl as e
import argparse
import time
import sys
import pandas as pd
import numpy as np
import geopandas as gpd


DB_SCHEMA = "ods"
TABLE = "originaldata"
TABLE_STATIONS = 'sensors_points'
TABLE_FRAGUESIAS = 'fraguesias'
#DOWNLOAD_DIR = "data/original"
#PROCESSED_DIR = "data/processed"
STATIC_DIR = "data/static"


def extraction(config: dict) -> pd.DataFrame:
    """ Runs extraction

        Args:
            config (str): configuration dictionary
    """
    t0 = time.time()
    e.info("EXTRACTION: START DATA EXTRACTION")
    url = config["url"]

    e.info("EXTRACTION: CREATING DATA FRAME")
    df = e.read_json(url)
    #you can check if is better to create a geodataframe instead of dataframe
    print(df["date"])

    e.info("EXTRACTION: COMPLETED")
    t1 = time.time()
    e.info("EXTRACTION TIME: " + str(t1-t0) + " seconds")
#     #sys.exit(0)
    return df

   
def transformation(config: dict, df: pd.DataFrame) -> pd.DataFrame:
    """Runs transformation

    Args:
        config (dict): [description]
    """
    t0 = time.time()
    e.info("TRANSFORMATION: START TRANSFORMATION")
    e.info("TRANSFORMATION: READING DATA")
    
    #unnest the dataframe in order to get the coordinates in separated columns
    print(df.columns)
    # only unnest the dataframe if we need the coordinates
    #unnested_df = df.join(pd.DataFrame(df.coordinates.tolist(),index=df.index).add_prefix('coordinates_'))

    columns_to_drop = ['avg', 'dateStandard', 'unit', 'address', 'coordinates', 'directions']
    df = df.drop(columns=columns_to_drop)
    df = df.astype({"date": 'str'})
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d%H%M').dt.date
    
    #df['date'] = df['date'].apply(pd.to_datetime(['date'], format='%Y%m%d%H%M'))

    print(df.columns)
    print(df.head())

    #create three dataframes, one for each variable    
    
    temp_df = df[df['id'].str.contains("METEMP")==True]
    hum_df = df[df['id'].str.contains("ME00HR")==True]
    noise_df = df[df['id'].str.contains("RULAEQ")==True]


    print("temp dataframe")
    print(temp_df.shape)
    print("noise df")
    print(noise_df.shape)
    print("humidity df")
    print(hum_df.shape)
   
    #creating a new dataframe which combines the enviromental variables and stations
    list_df = [temp_df, noise_df, hum_df]
          
    for i in list_df:
        
        i['id_sensor'] = i['id'].str[-4:]
        del i['id']
        i = i.set_index('id_sensor')
    
    
    
    print("temp removed columns")
    print(temp_df.head())
    print(temp_df.shape)
    print("noise removed columns")
    print(noise_df.head())
    print(noise_df.shape)
    print("humidity removed columns")
    print(hum_df.head())
    print(hum_df.shape)
    
    # importing stations file from static data
    stations = config["fname_stations"]
    gdf = e.read_geojson(f"{STATIC_DIR}/{stations}")
    print(gdf.head())
    
    
    stations_df = pd.DataFrame(gdf)
    columns_to_drop1 = ['address', 'geometry']
    stations_df = stations_df.drop(columns=columns_to_drop1)

    print(stations_df.head())


    stations_merged1 = pd.merge(stations_df, temp_df, how='left', on='id_sensor')
    stations_merged1.rename(columns={'value': 'temp_value','date': 'date_temp'}, inplace=True)

    stations_merged2 = pd.merge(stations_merged1, noise_df, how='left', on='id_sensor')
    stations_merged2.rename(columns={'value': 'noise_value','date': 'date_noise'}, inplace=True)

    stations_env_variables = pd.merge(stations_merged2, hum_df, how='left', on='id_sensor')
    stations_env_variables.rename(columns={'value': 'hum_value','date': 'date_hum'}, inplace=True)
    

    print(stations_env_variables.head())
    print(stations_env_variables.shape)
    
    print(stations_env_variables.dtypes)

    
    e.info("TRANSFORMATION: SUBSETTING DONE")    
    e.info("TRANSFORMATION: COMPLETED")
    
    ##########################################################################

    #Task create dataframe for STATION and covert to geodataframe  

    #stations_df = unnested_df[['id', 'coordinates_lat', 'coordinates_lng', 'address']]

    #stations_df["id_sensor"] = stations_df["id"].str[-4:]

    #del stations_df['id']

    #stations_df_f = stations_df.drop_duplicates()

    #changing columns order

    #stations_df_f = stations_df_f[['id_sensor', 'coordinates_lat', 'coordinates_lng', 'address']]

    #print("keeping only last part of original id \n")
    #print(stations_df_f.head())
    #print(stations_df_f.shape)

    #convert stations_df_f to geodataframe

    #gdf_stations = gpd.GeoDataFrame(stations_df_f, geometry=gpd.points_from_xy(stations_df_f.coordinates_lng, stations_df_f.coordinates_lat))
 
    #print(gdf_stations.head())
    #print(gdf_stations.shape)
    
    ############################################################
    t1 = time.time()
    e.info("TRANSFORMATION TIME: " + str(t1-t0) + " seconds")
    return stations_env_variables


def load(config: dict, env_var: pd.DataFrame, chunksize: int=1000) -> None:
    """Runs load

    Args:
        config (dict): configuration dictionary
        env_var (string): returned dataframe from transformation operation
        chunksize (int): the number of rows to be inserted at one time
    """
    t0 = time.time()
    print(env_var.columns)
    print(env_var.head())

    try:

        connection = e.DBController(**config["database"])
        e.info("LOAD: READING DATA")
    
        e.info("LOAD: DATA READ")
        e.info("LOAD: INSERTING DATA INTO DATABASE")
        connection.insert_data(env_var, DB_SCHEMA, TABLE, chunksize=chunksize)


        
        e.info("LOAD: DONE")
        t1 = time.time()
        e.info("LOADING TIME: " + str(t1-t0) + " seconds")
    except Exception as err:
        e.die(f"LOAD: {err}")

def load_geodata(config: dict) -> None:

    """Runs load_geodata

    Args:
        config (dict): configuration dictionary
    
    """      
    e.info("UPLOADING GEOJSON FILES TO DATABASE")

    sensors = config["fname_stations"]
    gdf_sensors = e.read_geojson(f"{STATIC_DIR}/{sensors}")

    neighborhood = config["fname_fraguesias"]
    gdf_fraguesias = e.read_geojson(f"{STATIC_DIR}/{neighborhood}")


    try:
        connection = e.DBController(**config["database"])
        
        connection.insert_geodata(gdf_sensors, DB_SCHEMA, TABLE_STATIONS)
        e.info("UPLOADED SENSOR STATIONS POINTS")
        connection.insert_geodata(gdf_fraguesias, DB_SCHEMA, TABLE_FRAGUESIAS)
        e.info("UPLOADED FRAGUESIAS POLYGONS")

    except Exception as err:
        e.die(f"LOAD: {err}")



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
    """Main function for ETL

    Args:
        config_file (str): configuration file
    """
    config = e.read_config(config_file)
    df = extraction(config)
    
    env_var = transformation(config, df)
    
    load(config, env_var, chunksize=10000)
    
    load_geodata(config)
    

if __name__ == "__main__":
    config_file = parse_args()
    main(config_file)

