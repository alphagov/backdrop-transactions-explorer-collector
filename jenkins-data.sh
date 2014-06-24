#!/bin/bash

echo "Setting up a virtualenv and installing dependencies"

virtualenv ./virtualenv/
. ./virtualenv/bin/activate
pip install -r requirements.txt

echo "Collecting data from the spreadsheet"

echo "{\"transactions_explorer\": {\"username\": \"$GOOGLE_USERNAME\",\"password\": \"$GOOGLE_PASSWORD\",\"key\": \"$GOOGLE_SPREADSHEET_KEY\",\"worksheet\": \"$GOOGLE_SPREADSHEET_WORKSHEET\" } }" > config.json

./backdrop-transactions-explorer-collector transactions_explorer config.json > transactions-explorer-data.json

echo "Posting data to Backdrop"

curl $BACKDROP_ENDPOINT --request POST --header "Authorization: Bearer $BACKDROP_TOKEN" --header 'Content-type: application/json' --data @transactions-explorer-data.json

echo "Done."
