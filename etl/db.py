import datetime
from select import select
from sqlite3 import Cursor
from .logs import die
from geoalchemy2 import Geometry, WKTElement
import sqlalchemy as sql
import pandas as pd
import geopandas as gpd



class DBController:
    def __init__(self, host: str, port: str, database: str, username: str, password: str):
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.uri = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
        #self.uri = f"postgres+psycopg2://{username}:{password}@{host}:{port}/{database}"

    def select_data(self, query: str) -> pd.DataFrame:
        """This functions abstracts the `SELECT` queries

        Args:
            query (str): the select query to be executed

        Returns:
            pd.DataFrame: the selection
        """
        try:
            con = sql.create_engine(self.uri)
            select_df = pd.read_sql(query, con, parse_dates={ "date": {"format": "%Y-%m-%d"}})
        except Exception as e:
            die(f"select_data: {e}")
        return select_df

    def insert_data(self, df: pd.DataFrame, schema: str, table: str, chunksize: int=100) -> None:
        """This function abstracts the `INSERT` queries

        Args:
            df (pd.DataFrame): dataframe to be inserted
            schema (str): the name of the schema
            table (str): the name of the table
            chunksize (int): the number of rows to insert at the time
        """
        try:
            engine = sql.create_engine(self.uri)
            with engine.connect() as con:
                tran = con.begin()
                df.to_sql(
                    name=table, schema=schema,
                    con=con, if_exists="append", index=False,
                    chunksize=chunksize, method="multi"
                )
                tran.commit()
        except Exception as e:
            if 'tran' in locals():
                tran.rollback()
            die(f"{e}")
    
    def insert_geodata(self, gdf: gpd.GeoDataFrame, schema: str, table: str) -> None:
        """This function abstracts the `INSERT` queries

        Args:
            df (pd.DataFrame): dataframe to be inserted
            schema (str): the name of the schema
            table (str): the name of the table
        """
        try:
            engine = sql.create_engine(self.uri)
            with engine.connect() as con:
                tran = con.begin()
                gdf.to_postgis(name=table, schema=schema, con=con, if_exists="replace", index=False)
                tran.commit()
        except Exception as e:
            if 'tran' in locals():
                tran.rollback()
            die(f"{e}")
    
    # def querydata(self, initial_date: datetime, final_date: datetime)-> pd.DataFrame: 

    #     """This functions abstracts the `SELECT` queries

    #     Args:
    #         initial_date (date): the initial date to be used in the query to be executed
    #         final_date (date)
    #     Returns:
    #         pd.DataFrame: the selection
    #     """
    #     try:
    #         engine = sql.create_engine(self.uri)
    #         #cursor = engine.cursor()
    #         dates = initial_date , final_date

    #         sql_statement = """select * from us.env_variables 
    #                         where (date_temp >= :initial_date 
    #                         or date_noise >= :initial_date or date_hum >= :initial_date)
    #                         and (date_temp <= :final_date 
    #                         or date_noise <= :final_date or date_hum <= :final_date)"""
            
            
    #         result = engine.execute(sql_statement, dates )

    #         for r in result:  
    #             print(r)
            

    #         #query_df = pd.read_sql(cursor)
    #         #cursor.close()
    #         #engine.close()
    #     except Exception as e:
    #         die(f"query_data: {e}")
        
        #return query_df






# Read
#result_set = db.execute("SELECT * FROM films")  
#for r in result_set:  
#    print(r)