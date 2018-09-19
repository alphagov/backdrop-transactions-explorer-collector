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
    echo "Have you downloaded The Spreadsheet™?"
    exit 3
fi

set -u

pip install -r requirements.txt
pip install -r requirements_csv.txt
pip install https://github.com/alphagov/backdropsend/tarball/0.0.1

./backdrop-transactions-explorer-collector tools/data/services.csv > /tmp/btec.json

json_items="$(jq 'length' /tmp/btec.json)"
items_per_post=1000

for i in $(seq 0 $((( json_items / items_per_post )))); do
  start_index="$((( i * items_per_post )))"
  end_index="$((( start_index + items_per_post )))"

  echo "Sending records ${start_index}-${end_index}..."
  # this is because backdrop-send is weird
  jq  ".[${start_index}:${end_index}]" /tmp/btec.json > /tmp/btec-current.json
  backdrop-send \
    --url "https://${backdrop_fqdn}/data/transactional-services/summaries" \
    --token "${backdrop_access_token}" \
    --timeout 120 \
    < /tmp/btec-current.json
done

cd tools
python create_transaction_volumes_csv.py
cd ..

echo "Completed successfully."
echo -n "The files tools/data/services.csv and tools/data/transaction-volumes.csv "
echo "can now be updated in spotlight (assets/data)."
