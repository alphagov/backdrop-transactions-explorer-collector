# -*- coding: utf-8 -*-
import base64
import datetime
import json
import sys
from classes.transactions_explorer_data_type import TransactionsExplorerDataType
from classes.service import Service


def setup_data_types():
    # Each service contains 2 different ways of returning data: quarterly,
    # and seasonally adjusted. Each of the 2 ways of returning data is
    # available for 5 time periods.

    # Seasonally adjusted data has a duration of 1 year and contains 4 metrics.
    # Every year the spreadsheet takes the latest quarterly data and adds it to
    # that of the previous 3 quarters to come up with new seasonally adjusted
    # data point.

    # For seasonally adjusted data, the keys used to extract the data
    # (e.g. 2014-Q4) represent when the data was *requested* not the
    # period which the data is for. The period the data is for is normally
    # the one before the one implied by the key. As a result the start at
    # for 2014-Q4 is October 2013 rather than January 2014.

    # 2012-Q4 is a special case of trial data collection and so does not fall
    # into the normal pattern. It was requested in 2012-Q4 but represents the
    # time period below (April 2011 to March 2012)

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
            '2014-Q1': {
                '_start_at': datetime.datetime(2013, 01, 01, 0, 0),
                '_end_at': datetime.datetime(2014, 01, 01, 0, 0),
            },
            '2014-Q2': {
                '_start_at': datetime.datetime(2013, 04, 01, 0, 0),
                '_end_at': datetime.datetime(2014, 04, 01, 0, 0),
            },
            '2014-Q3': {
                '_start_at': datetime.datetime(2013, 07, 01, 0, 0),
                '_end_at': datetime.datetime(2014, 07, 01, 0, 0),
            },
            '2014-Q4': {
                '_start_at': datetime.datetime(2013, 10, 01, 0, 0),
                '_end_at': datetime.datetime(2014, 10, 01, 0, 0),
            },
            '2015-Q1': {
                '_start_at': datetime.datetime(2014, 01, 01, 0, 0),
                '_end_at': datetime.datetime(2015, 01, 01, 0, 0),
            },
            '2015-Q2': {
                '_start_at': datetime.datetime(2014, 04, 01, 0, 0),
                '_end_at': datetime.datetime(2015, 04, 01, 0, 0),
            },
            '2015-Q3': {
                '_start_at': datetime.datetime(2014, 07, 01, 0, 0),
                '_end_at': datetime.datetime(2015, 07, 01, 0, 0),
            },
            '2015-Q4': {
                '_start_at': datetime.datetime(2014, 10, 01, 0, 0),
                '_end_at': datetime.datetime(2015, 10, 01, 0, 0),
            },
            '2016-Q1': {
                '_start_at': datetime.datetime(2015, 01, 01, 0, 0),
                '_end_at': datetime.datetime(2016, 01, 01, 0, 0),
            },
            '2016-Q2': {
                '_start_at': datetime.datetime(2015, 04, 01, 0, 0),
                '_end_at': datetime.datetime(2016, 04, 01, 0, 0),
            },
            '2016-Q3': {
                '_start_at': datetime.datetime(2015, 07, 01, 0, 0),
                '_end_at': datetime.datetime(2016, 07, 01, 0, 0),
            },
            '2016-Q4': {
                '_start_at': datetime.datetime(2015, 10, 01, 0, 0),
                '_end_at': datetime.datetime(2016, 10, 01, 0, 0),
            },
            '2017-Q1': {
                '_start_at': datetime.datetime(2016, 01, 01, 0, 0),
                '_end_at': datetime.datetime(2017, 01, 01, 0, 0),
            },
            '2017-Q2': {
                '_start_at': datetime.datetime(2016, 04, 01, 0, 0),
                '_end_at': datetime.datetime(2017, 04, 01, 0, 0),
            },
            '2017-Q3': {
                '_start_at': datetime.datetime(2016, 07, 01, 0, 0),
                '_end_at': datetime.datetime(2017, 07, 01, 0, 0),
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
            # The following field is not stored in the spreadsheet,
            # it is calculated below
            u'Digital take-up': 'digital_takeup',
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
            'Oct - Dec 2013': {
                '_start_at': datetime.datetime(2013, 10, 01, 0, 0),
                '_end_at': datetime.datetime(2014, 01, 01, 0, 0),
            },
            'Jan - Mar 2014': {
                '_start_at': datetime.datetime(2014, 01, 01, 0, 0),
                '_end_at': datetime.datetime(2014, 04, 01, 0, 0),
            },
            'Apr - Jun 2014': {
                '_start_at': datetime.datetime(2014, 04, 01, 0, 0),
                '_end_at': datetime.datetime(2014, 07, 01, 0, 0),
            },
            'Jul - Sep 2014': {
                '_start_at': datetime.datetime(2014, 07, 01, 0, 0),
                '_end_at': datetime.datetime(2014, 10, 01, 0, 0),
            },
            'Oct - Dec 2014': {
                '_start_at': datetime.datetime(2014, 10, 01, 0, 0),
                '_end_at': datetime.datetime(2015, 01, 01, 0, 0),
            },
            'Jan - Mar 2015': {
                '_start_at': datetime.datetime(2015, 01, 01, 0, 0),
                '_end_at': datetime.datetime(2015, 04, 01, 0, 0),
            },
            'Apr - Jun 2015': {
                '_start_at': datetime.datetime(2015, 04, 01, 0, 0),
                '_end_at': datetime.datetime(2015, 07, 01, 0, 0),
            },
            'Jul - Sep 2015': {
                '_start_at': datetime.datetime(2015, 07, 01, 0, 0),
                '_end_at': datetime.datetime(2015, 10, 01, 0, 0),
            },
            'Oct - Dec 2015': {
                '_start_at': datetime.datetime(2015, 10, 01, 0, 0),
                '_end_at': datetime.datetime(2016, 01, 01, 0, 0),
            },
            'Jan - Mar 2016': {
                '_start_at': datetime.datetime(2016, 01, 01, 0, 0),
                '_end_at': datetime.datetime(2016, 04, 01, 0, 0),
            },
            'Apr - Jun 2016': {
                '_start_at': datetime.datetime(2016, 04, 01, 0, 0),
                '_end_at': datetime.datetime(2016, 07, 01, 0, 0),
            },
            'Jul - Sep 2016': {
                '_start_at': datetime.datetime(2016, 07, 01, 0, 0),
                '_end_at': datetime.datetime(2016, 10, 01, 0, 0),
            },
            'Oct - Dec 2016': {
                '_start_at': datetime.datetime(2016, 10, 01, 0, 0),
                '_end_at': datetime.datetime(2017, 01, 01, 0, 0),
            },
            'Jan - Mar 2017': {
                '_start_at': datetime.datetime(2017, 01, 01, 0, 0),
                '_end_at': datetime.datetime(2017, 04, 01, 0, 0),
            },
            'Apr - Jun 2017': {
                '_start_at': datetime.datetime(2017, 04, 01, 0, 0),
                '_end_at': datetime.datetime(2017, 07, 01, 0, 0),
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
                        metric_value = service.get_datum(metric_key)
                    else:
                        if metric == 'Total cost':
                            number_of_transactions = service.get_datum(data_type.get_key('Vol.', period))
                            cpt = service.get_datum(data_type.get_key(u'CPT', period))

                            if number_of_transactions == None or cpt == None:
                                metric_value = None
                            else:
                                metric_value = (number_of_transactions * cpt)

                        elif metric == 'Digital take-up':
                            number_of_transactions = service.get_datum(data_type.get_key(data_type.get_spreadsheet_title_from_metric('number_of_transactions'), period))
                            number_of_digital_transactions = service.get_datum(data_type.get_key(data_type.get_spreadsheet_title_from_metric('number_of_digital_transactions'), period))

                            if not number_of_transactions:
                                metric_value = None
                            elif number_of_digital_transactions == 0:
                                metric_value = 0
                            elif number_of_digital_transactions == None:
                                metric_value = None
                            else:
                                metric_value = (number_of_digital_transactions / (number_of_transactions + 0.0))

                    tidy_metric_name = data_type.metrics[metric]
                    datum[tidy_metric_name] = metric_value

                formatted_data.append(datum)

    return formatted_data
