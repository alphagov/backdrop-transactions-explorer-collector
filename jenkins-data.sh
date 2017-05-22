#!/bin/bash

set -eo pipefail

echo "Setting up a virtualenv and installing dependencies"

virtualenv ./virtualenv/
. ./virtualenv/bin/activate
./virtualenv/bin/pip install --upgrade pip wheel
./virtualenv/bin/pip install -r requirements.txt

echo "Collecting data from the spreadsheet"

echo "{\"transactions_explorer\": {\"credentials\": $GOOGLE_CREDENTIALS,\"key\": \"$GOOGLE_SPREADSHEET_KEY\",\"worksheet\": \"$GOOGLE_SPREADSHEET_WORKSHEET\" } }" > config.json

# disabling warnings because an old version of python and urllib3. script otherwise exits.
# https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
export PYTHONWARNINGS="ignore"
./backdrop-transactions-explorer-collector transactions_explorer config.json > transactions-explorer-data.json 2>errors.txt

echo "Posting data to Backdrop"

curl --fail $BACKDROP_ENDPOINT --request POST --header "Authorization: Bearer $BACKDROP_TOKEN" --header 'Content-type: application/json' --data @transactions-explorer-data.json

echo "Done."
