from .logs import die
#import requests
import pandas as pd
import geopandas as gpd
import datetime

def read_json(url: str) -> pd.DataFrame:
    """Reads a JSON into a Pandas dataframe

    Args:
        fname (str): the name of the CSV file
        indicators (pd.DataFrame): the indicators we want
        sep (str, optional): the character separator. Defaults to ",".

    Returns:
        pd.DataFrame: [description]
    """
    try:
        df = pd.read_json(url, convert_dates = False)
        
    except Exception as e:
        die(f"read_json: {e}")
    return df

def read_geojson(fname: str) -> gpd.GeoDataFrame:
     """Reads a Geojson into a GeoPandas dataframe

     Args:
         fname (str): the name of the Geojson file
         indicators (gpd.GeoDataFrame): the indicators we want
         sep (str, optional): the character separator. Defaults to ",".

     Returns:
         gpd.GeoDataFrame: [description]
     """
     try:
         gdf = gpd.read_file(fname)
     except Exception as e:
         die(f"read_geojson: {e}")
     return gdf


