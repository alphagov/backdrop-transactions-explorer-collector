#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
from oauth2client import tools
from re import sub
from decimal import Decimal, InvalidOperation


CSV_FORMAT = [("Department", lambda s: s.department),
              ("Department Abbreviation", lambda s: s.abbr),
              ("Body/Agency", lambda s: s.body),
              ("Agency Abbreviation", lambda s: s.agency_abbr),
              ("Name of service", lambda s: s.name),
              ("April 2011 to March 2012: volume",
               lambda s: as_number(getattr(s, "2012_q4_vol"))),
              ("April 2011 to March 2012: digital volume",
               lambda s: as_number(getattr(s, "2012_q4_digital_vol"))),
              ("April 2011 to March 2012: cost per transaction (£)",
               lambda s: as_number(getattr(s, "2012_q4_cpt"))),
              ("January 2012 to December 2012: volume",
               lambda s: as_number(getattr(s, "2013_q1_vol"))),
              ("January 2012 to December 2012: digital volume",
               lambda s: as_number(getattr(s, "2013_q1_digital_vol"))),
              ("January 2012 to December 2012: cost per transaction (£)",
               lambda s: as_number(getattr(s, "2013_q1_cpt"))),
              ("April 2012 to March 2013: volume",
               lambda s: as_number(getattr(s, "2013_q2_vol"))),
              ("April 2012 to March 2013: digital volume",
               lambda s: as_number(getattr(s, "2013_q2_digital_vol"))),
              ("April 2012 to March 2013: cost per transaction (£)",
               lambda s: as_number(getattr(s, "2013_q2_cpt"))),
              ("July 2012 to June 2013: volume",
               lambda s: as_number(getattr(s, "2013_q3_vol"))),
              ("July 2012 to June 2013: digital volume",
               lambda s: as_number(getattr(s, "2013_q3_digital_vol"))),
              ("July 2012 to June 2013: cost per transaction (£)",
               lambda s: as_number(getattr(s, "2013_q3_cpt"))),
              ("October 2012 to September 2013: volume",
               lambda s: as_number(getattr(s, "2013_q4_vol"))),
              ("October 2012 to September 2013: digital volume",
               lambda s: as_number(getattr(s, "2013_q4_digital_vol"))),
              ("October 2012 to September 2013: cost per transaction (£)",
               lambda s: as_number(getattr(s, "2013_q4_cpt"))),
              ("January 2013 to December 2013: volume",
               lambda s: as_number(getattr(s, "2014_q1_vol"))),
              ("January 2013 to December 2013: digital volume",
               lambda s: as_number(getattr(s, "2014_q1_digital_vol"))),
              ("January 2013 to December 2013: cost per transaction (£)",
               lambda s: as_number(getattr(s, "2014_q1_cpt"))),
              ("April 2013 to March 2014: volume",
               lambda s: as_number(getattr(s, "2014_q2_vol"))),
              ("April 2013 to March 2014: digital volume",
               lambda s: as_number(getattr(s, "2014_q2_digital_vol"))),
              ("April 2013 to March 2014: cost per transaction (£)",
               lambda s: as_number(getattr(s, "2014_q2_cpt"))),
              ("July 2013 to June 2014: volume",
               lambda s: as_number(getattr(s, "2014_q3_vol"))),
              ("July 2013 to June 2014: digital volume",
               lambda s: as_number(getattr(s, "2014_q3_digital_vol"))),
              ("July 2013 to June 2014: cost per transaction (£)",
               lambda s: as_number(getattr(s, "2014_q3_cpt"))),
              ("October 2013 to September 2014: volume",
               lambda s: as_number(getattr(s, "2014_q4_vol"))),
              ("October 2013 to September 2014: digital volume",
               lambda s: as_number(getattr(s, "2014_q4_digital_vol"))),
              ("October 2013 to September 2014: cost per transaction (£)",
               lambda s: as_number(getattr(s, "2014_q4_cpt"))),
              ("January 2014 to December 2015: volume",
               lambda s: as_number(getattr(s, "2015_q1_vol"))),
              ("January 2014 to December 2015: digital volume",
               lambda s: as_number(getattr(s, "2015_q1_digital_vol"))),
              ("January 2014 to December 2015: cost per transaction (£)",
               lambda s: as_number(getattr(s, "2015_q1_cpt"))),
              ("April 2014 to March 2015: volume",
               lambda s: as_number(getattr(s, "2015_q2_vol"))),
              ("April 2014 to March 2015: digital volume",
               lambda s: as_number(getattr(s, "2015_q2_digital_vol"))),
              ("April 2014 to March 2015: cost per transaction (£)",
               lambda s: as_number(getattr(s, "2015_q2_cpt"))),
              ("July 2014 to June 2015: volume",
               lambda s: as_number(getattr(s, "2015_q3_vol"))),
              ("July 2014 to June 2015: digital volume",
               lambda s: as_number(getattr(s, "2015_q3_digital_vol"))),
              ("July 2014 to June 2015: cost per transaction (£)",
               lambda s: as_number(getattr(s, "2015_q3_cpt"))),
              ("October 2014 to September 2015: volume",
               lambda s: as_number(getattr(s, "2015_q4_vol"))),
              ("October 2014 to September 2015: digital volume",
               lambda s: as_number(getattr(s, "2015_q4_digital_vol"))),
              ("October 2014 to September 2015: cost per transaction (£)",
               lambda s: as_number(getattr(s, "2015_q4_cpt"))),
              ("January 2015 to December 2015: volume",
               lambda s: as_number(getattr(s, "2016_q1_vol"))),
              ("January 2015 to December 2015: digital volume",
               lambda s: as_number(getattr(s, "2016_q1_digital_vol"))),
              ("January 2015 to December 2015: cost per transaction (£)",
               lambda s: as_number(getattr(s, "2016_q1_cpt"))),
              ("April 2015 to March 2016: volume",
               lambda s: as_number(getattr(s, "2016_q2_vol"))),
              ("April 2015 to March 2016: digital volume",
               lambda s: as_number(getattr(s, "2016_q2_digital_vol"))),
              ("April 2015 to March 2016: cost per transaction (£)",
               lambda s: as_number(getattr(s, "2016_q2_cpt"))),
              ("July 2015 to June 2016: volume",
               lambda s: as_number(getattr(s, "2016_q3_vol"))),
              ("July 2015 to Juhe 2016: digital volume",
               lambda s: as_number(getattr(s, "2016_q3_digital_vol"))),
              ("July 2015 to June 2016: cost per transaction (£)",
               lambda s: as_number(getattr(s, "2016_q3_cpt"))),
              ("Service Type", lambda s: s.category),
              ("URL", lambda s: s.url),
              ("Description of service", lambda s: s.description),
              ("Notes on costs", lambda s: s.notes_on_costs),
              ("Other notes", lambda s: s.other_notes),
              ("Customer type", lambda s: s.customer_type),
              ("Business model", lambda s: s.business_model)]


def _create_parser():
    return argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        parents=[tools.argparser])


def create_directory(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


def keyify(text):
    unclean = sub(r'\W+', '_', text.lower())
    more_clean = sub(r'_$', '', unclean)
    return sub(r'^_', '', more_clean)


def as_number(num):
    if num:
        just_numbers = sub(r'[^\d\.]+', '', num)
        try:
            return Decimal(just_numbers)
        except InvalidOperation:
            pass
    return None


def encode(value):
    if isinstance(value, basestring):
        return value.encode('utf8')
    else:
        return value


def tabular_map(mappings, services):
    column_name = lambda m: m[0]

    def apply_mappings(service):
        return [encode(fn(service)) for _, fn in mappings]

    columns = map(column_name, mappings)

    return [columns] + map(apply_mappings, services)


def map_services_to_csv_data(services):
    return tabular_map(
        CSV_FORMAT,
        services
    )
