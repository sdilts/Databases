#!/bin/bash

# download the files:
./get-data.sh data
# initialize the database:
cat create-db.sql | sqlite3 imbd.db

# import the database:
./import-db.py data imbd.db
# kaggle isn't automatically downloaded, so don't run this:
# ./import-kaggle.py data imbd.db
