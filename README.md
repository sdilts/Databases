# Databases
Code needed for the CSCI-440 project
## Importing the database
  You can download and import the database using the `download-and-import.sh` script.
  This does everything to have a working database that is ready to use.
### Other scripts
  + `get-data.sh`: Downloads the imbd dataset from the IMBD website. It expects the location to place 
    the downloaded files as its first argument.
  + `import-db.py` and `import-kaggle.py`: Imports the respective data into a specified database. Both 
    scripts expect the data directory as their first argument. The second argument is the name of the 
    initialized sqlite database file. Note that the kaggle dataset isn't automatically downloaded by `get-data.sh`.
    To change the names of the files that are expected, see the `jobs` variable located in each file.
