# -*- coding: utf-8 -*-
import gspread
import argparse
import json
from oauth2client.client import SignedJwtAssertionCredentials


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('doc', help="The key in the configuration file for "
                                    "the document you want")
    parser.add_argument('config', help="The configuration file")
    return parser.parse_args(args)


def get_google_spreadsheet_data(credentials, key, worksheet):
    client_email = credentials['client_email']
    private_key = credentials['private_key']
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = SignedJwtAssertionCredentials(
        client_email,
        private_key,
        scope)

    google = gspread.authorize(credentials)
    spreadsheet = google.open_by_key(key)

    return spreadsheet.worksheet(worksheet).get_all_values()


def tidy_transactions_explorer_headers(data):
    """Removes pound signs from the end of
       Transactions Explorer headers, because string encoding
       is never fun"""

    tidy_data = []

    for element in data:
        element = element.replace(u'(£)', '').strip()
        tidy_data.append(element)

    return tidy_data


def convert_to_records(data):
    """Transforms a list of lists into a list of dictionaries, where data[0]
       is the header row of data"""
    header, rows = data[0], data[1:]

    header = tidy_transactions_explorer_headers(header)

    def process_cell(s):
        try:
            return int(s)
        except (ValueError, TypeError):
            try:
                return float(s)
            except (ValueError, TypeError):
                return s

    def row_to_dict(row):
        converted_row = map(process_cell, row)
        return dict(zip(header, converted_row))

    return map(row_to_dict, rows)


def spreadsheet_to_dictionary(args):
    arguments = parse_args(args)
    with open(arguments.config) as f:
        config = json.loads(f.read())
        this_config = config[arguments.doc]
        raw_data = get_google_spreadsheet_data(
            this_config['credentials'],
            this_config['key'],
            this_config['worksheet'])

        return convert_to_records(raw_data)
