CREATE EXTENSION postgis;

/*
    CREATE SCHEMAS
    Original dta schema is the schema where the original data will be stored once it's extracted from
    the online source
    
    User schema is the schema in charge of solving the queries for creating the maps related to the 
    environmental variables .
*/
CREATE SCHEMA ods; -- original data schema
CREATE SCHEMA us; -- user schema