#!/usr/bin/env python

import httplib2
import os
import sys
import argparse
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run


def _create_parser():
    return argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)


def parse_args_for_fetch(args):
    parser = _create_parser()
    parser.add_argument('--client-secrets',
                        help='Google API client secrets JSON file',
                        default='data/client_secrets.json')
    parser.add_argument('--oauth-tokens',
                        help='Google API OAuth tokens file',
                        default='data/tokens.dat')

    return parser.parse_args(args)


def create_directory(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


arguments = parse_args_for_fetch(sys.argv[1:])

SPREADSHEET = '0AiLXeWvTKFmBdFpxdEdHUWJCYnVMS0lnUHJDelFVc0E'
SERVICES_SHEET = '58'
SERVICES_DATA_OUTPUT = 'data/services.csv'
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

%s

with information from the APIs Console <https://code.google.com/apis/console>.

""" % os.path.join(os.path.dirname(__file__), arguments.client_secrets)


flow = flow_from_clientsecrets(
    arguments.client_secrets,
    scope='https://docs.google.com/feeds/ https://docs.googleusercontent.com/ https://spreadsheets.google.com/feeds/',
    message=MISSING_CLIENT_SECRETS_MESSAGE,
)
storage = Storage(arguments.oauth_tokens)
credentials = storage.get()
if credentials is None or credentials.invalid:
  credentials = run(flow, storage)

http = httplib2.Http()
http = credentials.authorize(http)

service = build("drive", "v2", http=http)
spreadsheet = service.files().get(fileId=SPREADSHEET).execute()
download_url = spreadsheet.get('exportLinks')['application/pdf']
download_url = download_url[:-4] + "=csv"

resp, content = service._http.request(download_url + "&gid=" + SERVICES_SHEET)

create_directory(os.path.dirname(SERVICES_DATA_OUTPUT))
csvFile = open(SERVICES_DATA_OUTPUT, 'w')
csvFile.write(content)
csvFile.close()
