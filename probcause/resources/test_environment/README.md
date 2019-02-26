# test_environment
This folder is where tests are run, in particular the integration tests from the back end. The data here was generated from crime_data.csv, which can be found in probcause/resources/datasets.

Test server runs on port 8082.

- bdb_setup.py and train_model.py were used to import the data-set
- run_server_eternally.py runs the test server

Metadata about the Testing Database

DB File:	crime.bdb
Table Name:	CRIMEDATA
Columns:	ID, Case Number, Date, Block, IUCR, Primary Type, Description,
            Location Description, Arrest, Domestic, Beat, District, Ward, 
            Community Area, FBI Code, X Coordinate, Y Coordinate, Year, 
            Updated On, Latitude, Longitude, Location