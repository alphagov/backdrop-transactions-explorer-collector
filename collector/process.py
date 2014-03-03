# -*- coding: utf-8 -*-
import base64
import datetime
import json
import sys
from classes.transactions_explorer_data_type import TransactionsExplorerDataType
from classes.service import Service


def handle_bad_data(datum):
    # TODO: Should we be more explicit about non-requested (***) data?
    if datum == '' or datum == '-' or datum == '***':
        return None
    elif not isinstance(datum, (int, long, float, complex)):
        # If the value we get from the spreadsheet is not numeric, send
        # that to Backdrop as a null data point
        return None
    else:
        return datum


def setup_data_types():
    # Each service contains 2 different ways of returning data: quarterly,
    # and seasonally adjusted. Each of the 2 ways of returning data is
    # available for 5 time periods.

    # Seasonally adjusted data has a duration of 1 year and contains 4 metrics.
    # Every year the spreadsheet takes the latest quarterly data and adds it to
    # that of the previous 3 quarters to come up with new seasonally adjusted
    # data point.

    seasonally_adjusted = TransactionsExplorerDataType(
        'seasonally-adjusted', '{period} {metric}',
        {
            'Vol.': 'number-of-transactions',
            u'CPT (£)': 'cost-per-transaction',
            'Digital vol.': 'number-of-digital-transactions',
            u'Digital CPT (£)': 'digital-cost-per-transaction',
        },
        {
            '2012-Q4': {
                '_start_at': datetime.datetime(2011, 04, 01, 0, 0),
                '_end_at': datetime.datetime(2012, 04, 01, 0, 0),
            },
            '2013-Q1': {
                '_start_at': datetime.datetime(2012, 01, 01, 0, 0),
                '_end_at': datetime.datetime(2013, 01, 01, 0, 0),
            },
            '2013-Q2': {
                '_start_at': datetime.datetime(2012, 04, 01, 0, 0),
                '_end_at': datetime.datetime(2013, 04, 01, 0, 0),
            },
            '2013-Q3': {
                '_start_at': datetime.datetime(2012, 07, 01, 0, 0),
                '_end_at': datetime.datetime(2013, 07, 01, 0, 0),
            },
            '2013-Q4': {
                '_start_at': datetime.datetime(2012, 10, 01, 0, 0),
                '_end_at': datetime.datetime(2013, 10, 01, 0, 0),
            },
        }
    )

    # Quarterly data is more granular than seasonally-adjusted data but only
    # contains 2 metrics rather than 4. As the name implies, it has a duration
    # of 3 months.

    quarterly = TransactionsExplorerDataType(
        'quarterly', '{metric}\n{period}',
        {
            'Total transactions': 'number-of-transactions',
            'Digital transactions': 'number-of-digital-transactions',
        },
        {
            'Jul - Sep 2012': {
                '_start_at': datetime.datetime(2012, 07, 01, 0, 0),
                '_end_at': datetime.datetime(2012, 10, 01, 0, 0),
            },
            'Oct - Dec 2012': {
                '_start_at': datetime.datetime(2012, 10, 01, 0, 0),
                '_end_at': datetime.datetime(2013, 01, 01, 0, 0),
            },
            'Jan - Mar 2013': {
                '_start_at': datetime.datetime(2013, 01, 01, 0, 0),
                '_end_at': datetime.datetime(2013, 04, 01, 0, 0),
            },
            'Apr - Jun 2013': {
                '_start_at': datetime.datetime(2013, 04, 01, 0, 0),
                '_end_at': datetime.datetime(2013, 07, 01, 0, 0),
            },
            'Jul - Sep 2013': {
                '_start_at': datetime.datetime(2013, 07, 01, 0, 0),
                '_end_at': datetime.datetime(2013, 10, 01, 0, 0),
            },
        }
    )

    return [seasonally_adjusted, quarterly]


def process(data):
    """Sets up the class instances we need to process and outputs JSON"""

    data_types = setup_data_types()

    formatted_data = []

    for index, service in enumerate(data):
        service = Service(index, service)

        for data_type in data_types:
            for period in data_type.periods:
                start_at = data_type.get_period_start_date(period)
                end_at = data_type.get_period_end_date(period)
                service_id = service.identifier()

                datum_id = str(start_at) + str(end_at) + service_id.encode('utf-8')

                datum = {
                    '_id': base64.b64encode(datum_id),
                    '_start_at': start_at,
                    '_end_at': end_at,
                    'service-id': service_id,
                    'type': data_type.title,
                }

                for metric in data_type.metrics:
                    metric_key = data_type.get_key(metric, period)
                    metric_value = handle_bad_data(service.get(metric_key))

                    tidy_metric_name = data_type.metrics[metric]
                    datum[tidy_metric_name] = metric_value

                formatted_data.append(datum)

    return formatted_data
