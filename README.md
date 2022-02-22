![tempsnip](https://user-images.githubusercontent.com/99036519/154965295-c1aac7d9-bcbe-4c07-af10-b0ff46810e8c.png)

# Introduction
Air quality monitoring is extremely important in today’s world as it has a direct impact on human health. The monitoring of atmosphere is extremely important as the air quality is an important problem for large communities. The main requirements for analytical devices used for monitoring air quality include a long period of autonomic operation and portability.
           This application is designed based of python repository which aims to help various users access and analytical report of certain environmental variables within the Lisbon municipality. It collects data about HUMDITY, TEMPERATURE and NOISE within a particular time interval, processes it and produce an IDW map of the variable in the form of an analytical report.
# Objectives
This project is aimed at producing a pdf report which will show the behavior of some environmental variables in Lisbon. The pdf reports will contain maps for temperature, precipitation, and noise in Lisbon, based on the data from 80 stations, maps will be generated using IDW as interpolation method, and using points for locating the stations.
The main objective is to use several open-source resources to build a solution aimed at producing a pdf report which will show the behavior of some environmental variables in Lisbon. This is done by performing the following operations:
* Extract data from online repository from ***Camara de Lisboa*
* Transform the original data by doing some cleaning and spatial operations in order to get a new perspective of the original data.
* Load the data into a database.
* Query data using dates as an interval for retrieving data from the database
* Aggregate values for each station for the period interval selected
* Create an IDW (Inverse Distance Weighting) raster surfaces using each of the chosen variable based on the various sensor points to map and see the distribution of noise in the
* Display the values for each variable using a plotted raster surface color ramp
* Create a pdf report with the plots for each environmental variable.
* Grant users access to retrieve data from the database connection using API.
* Generate a GUI interface where the user executes the program.
___________________________________________________________________________________________
# Data /Database 
The data comes from “camera municipal de Lisboa” “lisboa-aberta” (http://lisboaaberta.cmlisboa.pt/index.php/pt/dados/conjuntos-de-dados) with sensors deployed in 80 locations for monitoring the environmental parameters across Lisbon municipality which were aggregated on a daily basis.The database contains variables populated through the Python code and then stored in a table within a SQL database. The first table contains information about the environmental variables, such as their full name, ID and date. In the same database, there is another table that defines the environmental variables, such as their full name, ID and date as well as the sensor ID freguesia and address, which is the user interface. The database is updated every day by a schedular that runs every six (6) hours initiated by the ETL process.
# System Requirements (How To Run The App)
•Python 3.10.2 or later.
• The following modules installed:  asyncio, constants, fiona , bounds, etl as e,  argparse, time, os, sys, pandas as pd, numpy as np, plotly. express as px,  geopandas as gpd, datetime, gdal,  rasterio, matplotlib. pyplot as plt pathlib, contextily .
• Postgress database.
• User interface.
Running the application
• Run Env_API.py in the console to start the program.
• PS: while the web browser is loading, info messages are being printed in the python console.
