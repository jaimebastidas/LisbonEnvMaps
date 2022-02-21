![tempsnip](https://user-images.githubusercontent.com/99036519/154965295-c1aac7d9-bcbe-4c07-af10-b0ff46810e8c.png)

# INTRODUCTION
Air quality monitoring is extremely important in today’s world as it has a direct impact on human health. The monitoring of atmosphere is extremely important as the air quality is an important problem for large communities. The main requirements for analytical devices used for monitoring air quality include a long period of autonomic operation and portability.
           This application is designed based of python repository which aims to help various users access and analytical report of certain environmental variables within the Lisbon municipality. It collects data about HUMDITY, TEMPERATURE and NOISE within a particular time interval, processes it and produce an IDW map of the variable in the form of an analytical report.



# OBJECTIVES

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
Please continue here:

we'll implement a simple **ETL package**. 

ETL stands for Extraction-Transform-Load, and, in practice, means the code we are about to write must:

* Extract data from one or many sources. These sources are typically databases, APIs, flat files like CSV, etc;
* Transform the original data to serve our goals;
* Load the transformed data into a database (actually not necessarily, but it will in our example). 

An ETL process is, more often than not, started automatically by some sort of job scheduler. In other words, ETL processes are scheduled to run win a predefined frequency (e.g. "every day at 01:30 AM", "At the 20th day of each month at 06:00 AM", etc). These runs extract new data, transform and load it into the database. 

Thus, our code cannot rely on human intervention during the process, but it has to report some how in case of a fatal error.

So, a complete ETL process must:

* Perform all extraction, transformation and loading without quering the user; 
* Report the current state of the process, and in case of error;
* Be able to deal with the incomming of new data.

You can read more about ETL [here](https://en.wikipedia.org/wiki/Extract,_transform,_load).

## Data

We'll be using the [NYC taxi dataset](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page). 

## Questions

1. How many rides took place on each day of January?
2. What is the average fare amount for rides with only one passenger in the first two weeks?
3. How many rides of each rate type took place in the month of January?
4. For each airport, 
    * How rides there? 
    * What's the average ride duration? 
    * What's the average cost? 
    * What's the average tip? 
    * What's the min, average and max number of passengers?
5. How many rides took place every 5 minutes for the first day of 2016?
6. How many rides on New Year’s morning originated from within 400m of Times Square, in 30 minute buckets?
