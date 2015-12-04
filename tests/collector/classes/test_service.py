# -*- coding: utf-8 -*-
import unittest
from collector.classes.service import sanitise_string
from collector.classes.service import Service
from hamcrest import *
from mock import patch
import sys


class TestService(unittest.TestCase):
    def setUp(self):
        self.service = Service(3, {
            u'Name of service': 'Magical test service',
            u'Slug': 'magical-test-service',
            u'Abbr': 'GDS',
            u'Weird Key': 456,
            u'Another Key (£)': 123,
        })

    def test_sanitise_string_removes_weird_character(self):
        messy_string = u'£123 '
        assert_that(sanitise_string(messy_string), is_(u'123'))

    @patch.object(Service, 'get')
    def test_get_datum_calls_get_with_the_key_name(self, service_get):
        service_get.return_value = 456
        datum = self.service.get_datum('Weird Key')
        service_get.assert_called_with('Weird Key')

    @patch.object(Service, 'handle_bad_data')
    def test_get_datum_calls_handle_bad_data_with_the_key_value(self, handle_bad_data):
        datum = self.service.get_datum('Weird Key')
        handle_bad_data.assert_called_with(456)

    def test_it_returns_an_identifier(self):
        identifier = self.service.identifier()
        assert_that(identifier, is_('magical-test-service'))

    def test_it_returns_a_datum(self):
        datum = self.service.get('Weird Key')
        assert_that(datum, is_(456))

    def test_bad_data_handles_strings_we_know_about(self):
        assert_that(self.service.handle_bad_data(''), is_(None))
        assert_that(self.service.handle_bad_data('-'), is_(None))
        assert_that(self.service.handle_bad_data('***'), is_(None))

    @patch('collector.classes.service.sys.stderr')
    def test_bad_data_handles_strings_we_dont_know_about(self, stderr):
        assert_that(self.service.handle_bad_data('foo'), is_(None))

    def test_bad_datatest_bad_data_handles_numbers(self):
        assert_that(self.service.handle_bad_data(345), is_(345))
