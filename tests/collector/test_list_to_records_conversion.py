# coding=utf8
import unittest
from hamcrest import *
from collector.csv_to_dictionary import _convert_to_records
import json


class TestListToRecordsConversion(unittest.TestCase):
    def test_it_converts_list_of_lists_into_records(self):
        data = [
            ['Column1', 'Column2', 'Column3'],
            ['Value11', 'Value12', 'Value13'],
            ['Value21', 'Value22', 'Value23'],
            ['Value31', 'Value32', 'Value33']
        ]
        expected_records = [
            {'Column1': 'Value11',
             'Column2': 'Value12',
             'Column3': 'Value13'},
            {'Column1': 'Value21',
             'Column2': 'Value22',
             'Column3': 'Value23'},
            {'Column1': 'Value31',
             'Column2': 'Value32',
             'Column3': 'Value33'}
        ]

        assert_that(_convert_to_records(data), is_(expected_records))

    def test_it_converts_an_integer_to_a_number(self):
        data = [
            ['IntegerColumn', 'StringColumn'],
            ['301', 'This is still a string']
        ]
        expected_records = [
            {
                u'IntegerColumn': 301,
                u'StringColumn': 'This is still a string'
            }
        ]

        assert_that(_convert_to_records(data), is_(expected_records))

    def test_it_converts_a_float_to_a_number(self):
        data = [
            ['FloatColumn', 'StringColumn'],
            ['42.75', 'This is still a string']
        ]
        expected_records = [
            {
                u'FloatColumn': 42.75,
                u'StringColumn': 'This is still a string'
            }
        ]

        assert_that(_convert_to_records(data), is_(expected_records))

    def test_it_handles_encoded_characters_correctly(self):
        data = [
            ['Heading1', u'Heading with pound sign \xa3', 'Heading3'],
            [u'\xa34.50', 'text', 'more text']
        ]
        expected_json = '[{"Heading with pound sign \u00a3": "text", ' \
                        '"Heading3": "more text", "Heading1": "\u00a34.50"}]'

        assert_that(json.dumps(_convert_to_records(data)), is_(expected_json))
