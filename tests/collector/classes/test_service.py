# -*- coding: utf-8 -*-
import unittest
from hamcrest import *
from collector.classes.service import sanitise_string
from collector.classes.service import Service


class TestService(unittest.TestCase):
    def setUp(self):
        self.service = Service(3, {
            u'Name of service': 'Magical test service',
            u'Abbr': 'GDS',
            u'Weird Key': 456,
            u'Another Key (£)': 123,
        })

    def test_sanitise_string_removes_weird_character(self):
        messy_string = u'£123 '
        assert_that(sanitise_string(messy_string), is_(u'123'))

    def test_it_returns_an_identifier(self):
        identifier = self.service.identifier()
        assert_that(identifier, is_('3 GDS Magical test service'))

    def test_it_returns_a_datum(self):
        datum = self.service.get('Weird Key')
        assert_that(datum, is_(456))
