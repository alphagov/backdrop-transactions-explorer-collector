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
