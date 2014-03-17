import datetime
import unittest
from hamcrest import *
from collector.classes.transactions_explorer_data_type import TransactionsExplorerDataType


class TestTransactionsExplorerDataType(unittest.TestCase):
    def setUp(self):
        self.data_type = TransactionsExplorerDataType(
            'title', '{period}---{metric}',
            {'Ugly Metric Name': 'nice-metric-name'},
            {
                'March 2014': {
                    '_start_at': datetime.datetime(2014, 03, 01),
                    '_end_at': datetime.datetime(2014, 04, 01),
                },
            },
        )

    def test_it_returns_a_correctly_formatted_key(self):
        formatted_key = self.data_type.get_key('Ugly Metric Name', 'March 2014')
        assert_that(formatted_key, is_('March 2014---Ugly Metric Name'))

    def test_it_returns_the_start_and_end_properties(self):
        start_date = self.data_type.get_period_start_date('March 2014')
        assert_that(start_date, is_(datetime.datetime(2014, 03, 01)))
        end_date = self.data_type.get_period_end_date('March 2014')
        assert_that(end_date, is_(datetime.datetime(2014, 04, 01)))
