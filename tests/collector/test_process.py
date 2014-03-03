# -*- coding: utf-8 -*-
import unittest
from hamcrest import *
from collector.classes.process import *


class TestProcess(unittest.TestCase):
    def test_it_handles_strings_we_know_about(self):
        assert_that(handle_bad_data(''), is_(None))
        assert_that(handle_bad_data('-'), is_(None))
        assert_that(handle_bad_data('***'), is_(None))

    def test_it_handles_strings_we_dont_know_about(self):
        assert_that(handle_bad_data('foo'), is_(None))

    def test_it_handles_numbers(self):
        assert_that(handle_bad_data(345), is_(345))
