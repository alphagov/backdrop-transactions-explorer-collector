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
            u'Vol.': 'number_of_transactions',
            u'CPT': 'cost_per_transaction',
            u'Digital vol.': 'number_of_digital_transactions',
            u'Digital CPT': 'digital_cost_per_transaction',
            # The following two fields are not stored in the spreadsheet,
            # they are calculated below
            u'Digital take-up': 'digital_takeup',
            u'Total cost': 'total_cost',
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
        },
        'year'
    )

    # Quarterly data is more granular than seasonally-adjusted data but only
    # contains 2 metrics rather than 4. As the name implies, it has a duration
    # of 3 months.

    quarterly = TransactionsExplorerDataType(
        'quarterly', '{metric}\n{period}',
        {
            u'Total transactions': 'number_of_transactions',
            u'Digital transactions': 'number_of_digital_transactions',
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
        },
        'quarter'
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
                period_duration = data_type.period_duration
                service_id = service.identifier()

                datum_id = str(start_at) + str(end_at) + service_id.encode('utf-8')

                datum = {
                    '_id': base64.b64encode(datum_id),
                    '_timestamp': start_at,
                    'end_at': end_at,
                    'period': period_duration,
                    'service_id': service_id,
                    'type': data_type.title,
                }

                for metric in data_type.metrics:

                    metric_key = data_type.get_key(metric, period)

                    if service.attribute_exists(metric_key):
                        metric_value = handle_bad_data(service.get(metric_key))
                    else:
                        if metric == 'Total cost':
                            number_of_transactions = handle_bad_data(service.get(data_type.get_key('Vol.', period)))
                            cpt = handle_bad_data(service.get(data_type.get_key(u'CPT', period)))

                            if number_of_transactions == None or cpt == None:
                                metric_value = None
                            else:
                                metric_value = (number_of_transactions * cpt)

                        elif metric == 'Digital take-up':
                            number_of_transactions = handle_bad_data(service.get(data_type.get_key('Vol.', period)))
                            number_of_digital_transactions = handle_bad_data(service.get(data_type.get_key('Digital vol.', period)))

                            if number_of_transactions == None or number_of_transactions == 0:
                                metric_value = None
                            elif number_of_digital_transactions == None or number_of_digital_transactions == 0:
                                metric_value = None
                            else:
                                metric_value = (number_of_digital_transactions / (number_of_transactions + 0.0))

                    tidy_metric_name = data_type.metrics[metric]
                    datum[tidy_metric_name] = metric_value

                formatted_data.append(datum)

    return formatted_data
