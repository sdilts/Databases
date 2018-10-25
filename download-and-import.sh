#!/bin/bash

# download the files:
./get-data.sh data
./import-db.py data imbd.db
# kaggle isn't automatically downloaded, so don't run this:
# ./import-kaggle.py data imbd.db
