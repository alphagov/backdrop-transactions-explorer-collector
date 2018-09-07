#!/usr/bin/env bash

set -eo pipefail

backdrop_fqdn=$1
backdrop_access_token=$2

if [ -z "${backdrop_fqdn}" ]
then
    echo "Backdrop FQDN needs to be provided!"
    exit 1
fi

if [ -z "${backdrop_access_token}" ]
then
    echo "Backdrop access token needs to be provided!"
    exit 2
fi

if [ ! -r "tools/data/services.csv" ]
then
    echo "'tools/data/services.csv' file not present / not readable."
    echo "Have you downloaded The Spreadsheet(TM)?"
    exit 3
fi

set -u

pip install -r requirements.txt
pip install -r requirements_csv.txt
pip install https://github.com/alphagov/backdropsend/tarball/0.0.1

./backdrop-transactions-explorer-collector tools/data/services.csv > /tmp/btec.json
backdrop-send --url "https://${backdrop_fqdn}/data/transactional-services/summaries" --token "${backdrop_access_token}" --timeout 120 < /tmp/btec.json

cd tools
python create_transaction_volumes_csv.py
cd ..

echo "Completed successfully."
echo -n "The files tools/data/services.csv and tools/data/transaction-volumes.csv "
echo "can now be updated in spotlight (assets/data)."
