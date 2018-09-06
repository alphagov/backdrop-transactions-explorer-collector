#!/usr/bin/env python
import argparse
import csv
import os
import sys
from distutils import dir_util

import unicodecsv
# from lib.filters import digest

from helper import create_parser
from helper import create_directory
from helper import map_services_to_csv_data
from service import Service


path_prefix = '/'
asset_prefix = '/transactions-explorer/'
static_prefix = 'https://assets.digital.cabinet-office.gov.uk/static'


def parse_args_for_create(args):
    parser = create_parser()
    parser.add_argument('--services-data',
                        help='Services CSV datafile',
                        default='data/services.csv')
    parser.add_argument('--path-prefix',
                        help='Prefix for generated URL paths',
                        default=path_prefix)
    parser.add_argument('--asset-prefix',
                        help='Prefix for generated asset URLs',
                        default=asset_prefix)
    parser.add_argument('--static-prefix',
                        help='Prefix for generated GOV.UK static URLs',
                        default=static_prefix)
    parser.add_argument('--static-digests',
                        help='Path to manifest file containing assets digests',
                        type=argparse.FileType())

    return parser.parse_args(args)


def render_csv(maps, out):
    with _output_file(out) as output:
        writer = csv.writer(output, dialect="excel")
        writer.writerows(maps)


def _output_file(path):
    print path
    output_path = os.path.join('', path)
    create_directory(os.path.dirname(output_path))
    return open(output_path, 'w')


arguments = parse_args_for_create(sys.argv[1:])
input = arguments.services_data

data = open(input)

reader = unicodecsv.DictReader(data)

services = [Service(details=row) for row in reader]

csv_map = map_services_to_csv_data(services)
render_csv(csv_map, 'data/transaction-volumes.csv')
