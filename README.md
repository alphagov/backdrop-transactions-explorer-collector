# Transactions Explorer collector for Backdrop

This Python app takes Transactions Explorer data from a Google Spreadsheet
and puts it into the [Performance Platform][pp] data store, [Backdrop][].

[pp]: https://www.gov.uk/performance
[Backdrop]: https://github.com/alphagov/backdrop

It is a more specific use case of the [backdrop-google-spreadsheet-collector][].

[backdrop-google-spreadsheet-collector]: https://github.com/alphagov/backdrop-google-spreadsheet-collector

## Setup

1. Get yourself a virtualenv (optional)
2. `pip install --allow-external argparse -r requirements_for_tests.txt`

## Running tests

`nosetests`

## Running the app

`./backdrop-google-spreadsheet-collector the_document_i_want config.json`

Create a `config.json` file in this directory that looks a bit like:

```json
{
  "the_document_i_want": {
    "username": "email@example.com",
    "password": "google-app-specific-password",
    "key": "google-docs-spreadsheet-key",
    "worksheet": "worksheet_title_from_google_spreadsheet_footer"
  }
}
```

This command will output JSON that can be consumed by other tools, eg piped
in to [backdropsend](https://github.com/alphagov/backdropsend).

## Fetching data

### Prerequisites

This README expects you to have the `virtualenv` and `virtualenvwrapper` python packages installed. You can do this with the following command.

```
pip install virtualenv virtualenvwrapper
```

You need to use a machine that has a web browser installed in order to
authenticate with Google. If you're using a GDS machine, this means you should
not perform any of these steps in the GDS development VM.

Set up a Python virtualenv, activate it, and then install required packages
with `pip install -r requirements_csv.txt`.

    $ cd ~/govuk
    $ cd backdrop-transactions-explorer-collector
    $ mkvirtualenv transactions-explorer
    $ pip install -r requirements_csv.txt

After setting this up for the first time, you just need to run
`workon transactions-explorer` in future.

### Running the job

First, ensure your Cabinet Office email account is authorised to access the
Transactions Explorer spreadsheet.

Then:

* Create a new installed application (of type "Native") in the [Google APIs console][console],
with "Drive API" service enabled, download the `client_secrets.json` file
and store it in `data/`
* On your base machine, activate a virtualenv.
* Install the prerequisites in requirements_csv.txt
* Fetch the data through either of the methods below:
  * In tools, Run `python fetch_csv.py`. This will authenticate against Google in your browser, then download the Transactions Explorer document to `data/services.csv`. It can be parametrized with the following arguments:
      * `--client-secrets`: Google API client secrets JSON file (default: `data/client_secrets.json`)
      * `--oauth-tokens`: Google API OAuth tokens file (default: `data/tokens.dat`)

