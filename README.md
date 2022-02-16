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





