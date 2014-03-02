import datetime
import json
import unittest
from hamcrest import *
from collector.classes.backdrop_json_encoder import BackdropJSONEncoder


class TestBackdropJSONEncoder(unittest.TestCase):
    def test_it_can_serialise_a_datetime(self):
        my_object = {
            'example_datetime': datetime.datetime(2014, 03, 02, 20, 46, 23)
        }
        my_object_as_json = '{"example_datetime": "2014-03-02T20:46:23+00:00"}'
        json_string = json.dumps(my_object, cls=BackdropJSONEncoder)
        assert_that(json_string, is_(my_object_as_json))

