import unittest
# from hamcrest import has_entries
from hamcrest.core import *
from tools.service import Service
from tools.helper import tabular_map


EXPECTED_DETAILS = [
    u'2012-Q4 Completion rate',
    u'2012-Q4 CPT (\xa3)',
    u'2012-Q4 Digital CPT (\xa3)',
    u'2012-Q4 Digital vol.',
    u'2012-Q4 User satisfaction',
    u'2012-Q4 Vol.',
    u'2012Q4 take-up',
    u'2013-Q1 Completion rate',
    u'2013-Q1 CPT (\xa3)',
    u'2013-Q1 Digital CPT (\xa3)',
    u'2013-Q1 Digital vol.',
    u'2013-Q1 User satisfaction',
    u'2013-Q1 Vol.',
    u'2013-Q2 Completion rate',
    u'2013-Q2 CPT (\xa3)',
    u'2013-Q2 Digital CPT (\xa3)',
    u'2013-Q2 Digital vol.',
    u'2013-Q2 User satisfaction',
    u'2013-Q2 Vol.',
    u'2013-Q3 Completion rate',
    u'2013-Q3 CPT (\xa3)',
    u'2013-Q3 Digital CPT (\xa3)',
    u'2013-Q3 Digital vol.',
    u'2013-Q3 User satisfaction',
    u'2013-Q3 Vol.',
    u'2013-Q4 Completion rate',
    u'2013-Q4 CPT (\xa3)',
    u'2013-Q4 Digital CPT (\xa3)',
    u'2013-Q4 Digital vol.',
    u'2013-Q4 User satisfaction',
    u'2013-Q4 Vol.',
    u'2013Q1 take-up',
    u'2014-Q1 Completion rate',
    u'2014-Q1 CPT (\xa3)',
    u'2014-Q1 Digital CPT (\xa3)',
    u'2014-Q1 Digital vol.',
    u'2014-Q1 User satisfaction',
    u'2014-Q1 Vol.',
    u'2014-Q2 Completion rate',
    u'2014-Q2 CPT (\xa3)',
    u'2014-Q2 Digital CPT (\xa3)',
    u'2014-Q2 Digital vol.',
    u'2014-Q2 User satisfaction',
    u'2014-Q2 Vol.',
    u'2014-Q3 Completion rate',
    u'2014-Q3 CPT (\xa3)',
    u'2014-Q3 Digital CPT (\xa3)',
    u'2014-Q3 Digital vol.',
    u'2014-Q3 User satisfaction',
    u'2014-Q3 Vol.',
    u'2014-Q4 Completion rate',
    u'2014-Q4 CPT (\xa3)',
    u'2014-Q4 Digital CPT (\xa3)',
    u'2014-Q4 Digital vol.',
    u'2014-Q4 User satisfaction',
    u'2014-Q4 Vol.',
    u'Abbr',
    u'Agency abbr',
    u'Agency/body',
    u'Business model',
    u'Category',
    u'CPT difference',
    u'Cumulative',
    u'Customer type',
    u'Data coverage \n(i.e. how many of 3 key data sets we have)',
    u'Department',
    u'Description of service',
    u'Detailed view?',
    u'FOI data',
    u'FOI text',
    u'FOI URL',
    u'GOV.UK start page',
    u'High-volume?',
    u'Keywords',
    u'Latest cost per transaction',
    u'Latest digital take-up',
    u'Latest digital total',
    u'Latest volumes',
    u'Name of service',
    u'No of electronic transactions',
    u'No of web transactions',
    u'Notes on costs',
    u'Notes [for GDS only]',
    u'Other notes',
    u'Percentage digital take-up\n2012 Q4',
    u'Percentage digital take-up\n2013 Q1',
    u'Short service name',
    u'Take-up difference',
    u'Total cost',
    u'URL',
]


def details(values):
    """
    Returns a dictionary of details to build a Service object, with all the
    expected properties; values for the returned dictionary can be provided
    as argument; if no value for a property is provided, it will default to
    None
    """
    return dict([(key, values.get(key)) for key in EXPECTED_DETAILS])


class TestCSV(unittest.TestCase):
    def test_csv_generation(self):
        services = [
            Service(details({"Name of service": "test_name", "Abbr": "tn"})),
            Service(details({"Name of service": "test_name_2", "Abbr": "tn2"}))
        ]

        table = tabular_map([("name_column", lambda s: s.name),
                             ("abbr", lambda s: s.abbr)],
                            services)

        assert_that(table, is_([["name_column", "abbr"],
                                ["test_name", "tn"],
                                ["test_name_2", "tn2"]]))

    def test_strings_get_utf8_encoded(self):
        services = [Service(details({"Name of service": u"\u2019"}))]

        table = tabular_map([("column", lambda s: s.name)], services)

        assert_that(table, is_([["column"], ["\xe2\x80\x99"]]))

