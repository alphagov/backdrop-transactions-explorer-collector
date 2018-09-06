# Transactions Explorer collector for Backdrop

This Python application takes Transactions Explorer data from a Google Spreadsheet
and puts it into the [Performance Platform][pp] data store, [Backdrop][].

[pp]: https://www.gov.uk/performance
[Backdrop]: https://github.com/alphagov/backdrop


NOTE - Before running it be sure to add new quarters and seasonally adjusted
fields to the application - see [commit][] by way of example and discuss which dates should be
added with the Performance Platform On-boarding team.

[commit]: https://github.com/alphagov/backdrop-transactions-explorer-collector/commit/dd5567f01bb9afcb0ea4190de015a91af550b18f

## Developer setup

1. Get yourself a virtualenv (optional)
2. `pip install --allow-external argparse -r requirements_for_tests.txt`

If you are using Mac OSX 10.x.x and encounter an error around the including of
`ffi.h` during the build, try running `xcode-select --install` in your terminal.

## Running tests

`nosetests`

## Run the thing

From here on "The Spreadsheet" refers to the transaction volume data maintained by
"Registers" at the time of writing.

1. Ensure you're in a virtualenv context.
1. Download the `TX_Data` (so named at time of writing) sheet from The Spreadsheet
as a csv as `tools/data/services.csv`.
1. Execute `./run.sh <backdrop_write_fqdn> <backrop_write_token>`.
1. Commit the resulting files (`tools/data/services.csv` and
`tools/data/transaction-volumes.csv`) into Spotlight (`assets/data`) and re-release Spotlight.

The `<backdrop_write_fqdn>` is the fully qualified domain name of the backdrop write
api (e.g. `performance-platform-backdrop-write-staging.cloudapps.digital` for staging).
The `<backdrop_write_token>` is the bearer token as specified in the stagecraft management
screens:

Stagecraft -> Data sets -> `transactional_services_summaries` -> Bearer token.
