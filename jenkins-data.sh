#!/bin/bash

set -eo pipefail

echo "Setting up a virtualenv and installing dependencies"

virtualenv ./virtualenv/
. ./virtualenv/bin/activate
./virtualenv/bin/pip install --upgrade pip wheel
./virtualenv/bin/pip install -r requirements.txt

echo "Setting up configuration"
echo "{\"transactions_explorer\": {\"credentials\": $GOOGLE_CREDENTIALS,\"key\": \"$GOOGLE_SPREADSHEET_KEY\",\"worksheet\": \"$GOOGLE_SPREADSHEET_WORKSHEET\" } }" > config.json

echo "Collecting data from the spreadsheet"
./backdrop-transactions-explorer-collector transactions_explorer config.json > transactions-explorer-data.json

echo "Posting data to Backdrop"
curl --fail $BACKDROP_ENDPOINT --request POST --header "Authorization: Bearer $BACKDROP_TOKEN" --header 'Content-type: application/json' --data @transactions-explorer-data.json

echo "Done."
