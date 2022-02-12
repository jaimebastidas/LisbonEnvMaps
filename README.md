# ETL - working example

## Objectives 

In this working example, we'll implement a simple **ETL package**. 

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

