# Transactions Explorer collector for Backdrop

This Python application takes Transactions Explorer data from a Google Spreadsheet
and puts it into the [Performance Platform][pp] data store, [Backdrop][].

[pp]: https://www.gov.uk/performance
[Backdrop]: https://github.com/alphagov/backdrop


The application achieves this with the help of a Jenkins job `jenkins-data.sh`, which is responsible
for:

1. Collecting the Transactions Explorer data from a Google spreadsheet which
is maintained by the on-boarding team;
2. Posting the collected data into the Backdrop application.

It is a more specific use case of the [backdrop-google-spreadsheet-collector][].

NOTE - Before running the Jenkins job, be sure to add new quarters and seasonally adjusted
fields to the application - see [commit][] by way of example and discuss which dates should be
added with the Performance Platform On-boarding team.

[commit]: https://github.com/alphagov/backdrop-transactions-explorer-collector/commit/dd5567f01bb9afcb0ea4190de015a91af550b18f

[backdrop-google-spreadsheet-collector]: https://github.com/alphagov/backdrop-google-spreadsheet-collector

## Developer setup

1. Get yourself a virtualenv (optional)
2. `pip install --allow-external argparse -r requirements_for_tests.txt`

If you are using Mac OSX 10.x.x and encounter an error around the including of
`ffi.h` during the build, try running `xcode-select --install` in your terminal.

## Running tests

`nosetests`

## Fetching transactions explorer data from a development machine

As a developer, you might want to fetch the transactions explorer data from
the Google spreadsheet so as to mimic step (1) of the Jenkins job, summarised above.
To do so:

1. Get access to the Google spreadsheet
2. Create an import configuration file
3. Run the application

### Get access to the Google spreadsheet

When the application is run, its first task is to collect data from the Google spreadsheet and
convert this data into a dict for further processing before posting to Backdrop.

Access to the Google spreadsheet is via OAuth 2.0 using the Python `oauth2client`. For this,
you will need a Google Service Account, which is an account that belongs to an application
instead of an individual end user.

You can set up a Service Account in the Google Development Console. Simply log in,
create a project and then add Service Account credentials for this project of key
type 'JSON'. Download the JSON credentials files.

Now ask the on-boarding team to grant access to the Google spreadsheet for the client
email address that can be found in JSON credentials file.

### Create an import configuration file

In the application's root directory, create a `config.json` file with the following
content:

```json
{
  "transactions_explorer_feed": {
    "credentials": {
      "client_email": "<from Service Account JSON file>",
      "private_key": "<from Service Account JSON file>"
    },
    "key": "<from URL of Google spreadsheet>",
    "worksheet": "name of the data worksheet on the Google spreadsheet"
  }
}
```

### Run the application

To run the application, type the following from within the application's
on your host:

`./backdrop-transactions-explorer-collector transactions_explorer_feed config.json`

This command will output JSON that can be consumed by other tools, eg piped
in to [backdropsend](https://github.com/alphagov/backdropsend).

## Getting data for CSV download

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

### Extracting Transactions Explorer data into a CSV file

Firstly, ensure your Cabinet Office email account is authorised to access the
Transactions Explorer spreadsheet.

Next, create and download a client secrets file:

* Log into the [Google Developers Console][google console] using your Cabinet Office email account
* Create a new project called, for example, Backdrop TX Collector
* Search for 'Drive API' and click the Drive API option that will be returned
* You should then be taken to the API Manager area
* Now click the Enable API button
* Click on the 'Credentials' options in the menu on the left-hand side of the page
* Click the 'New credentials' button to reveal a list of credential types
* Choose 'OAuth client ID'
* Click the 'Configure consent screen' button
* Now just enter a product name - it can be anything - and click Save
* You will then be asked to choose an Application type. Choose 'Other' and enter any name
* Click Create to reveal your client id and client secret, and then click OK
* You will then see a list of your OAuth 2.0 client IDs
* Click on the download icon against the client ID you just created
* A JSON client secret file will be downloaded
* Move this file to `tools/data` in backdrop-transactions-explorer-collector
* Rename the file to client_secrets.json

[google console]: https://console.developers.google.com/

Finally, run a script to create a CSV file representation of the data in the Transactions Explorer spreadsheet:

* On your base machine, activate your virtualenv
* Install the prerequisites in requirements_csv.txt
* From the tools directory, run `python fetch_csv.py`. This will authenticate against Google in your browser, then download the Transactions Explorer document to `data/services.csv`. It can be parameterised with the following arguments:
      * `--client-secrets`: Google API client secrets JSON file (default: `data/client_secrets.json`)
      * `--oauth-tokens`: Google API OAuth tokens file (default: `data/tokens.dat`)

### Creating a CSV for download

First, ensure that you have a services.csv file in the tools/data directory. If not, run the fetch_csv script as detailed above.

* On your base machine, activate a virtualenv
* Install the prerequisites in requirements_csv.txt
* From the tools directory, run `python create_transaction_volumes_csv.py`. This will transform and run calculations against the data in `data\services.csv` and then save it to `data\transaction-volumes.csv`. It can be parameterised with the following arguments:
      * `--services-data`: Services CSV datafile (default: `data/services.csv`)
      * `--path-prefix`: Prefix for generated URL paths (default: `/`)
      * `--asset-prefix`: Prefix for generated asset URLs (default: `/transactions-explorer/`)
      * `--static-prefix`: Path to manifest file containing assets digests


