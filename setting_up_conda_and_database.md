# How to create the conda environment

1. Start by installing miniconda, you can use all the defaults.
2. Once it's done, open the anaconda prompt
3. type the following to create a new environment
    
   ```
   conda create -n etl_example
   ```

4. To activate the new environment, type:

   ```
   conda activate etl_example
   ```
   
   You can run this command from any folder, it does not matter.

5. Using the `cd` commands, navigate to the 08 - ETL Example folder
6. To install all the dependencies, type:

   ```
   conda install --file requirements.txt --channel conda-forge
   ```
   
   This will install all the dependencies from conda-forge channel

7. Now, everything should be in place for running tghe example.

# Create the database

To run the code, we will need to setup a database called taxidb. You can try creating it by yourself.

1. Using PgAdmin4, create a new database called `taxidb`
2. Open the query tool for that database.
3. By order, load and run each of the .sql files that are inside the `db` folder (00-create-schemas.sql, ...)
