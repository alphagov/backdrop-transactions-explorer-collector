import json
import tempfile
import unittest
from mock import patch
from collector.spreadsheet_to_dictionary import spreadsheet_to_dictionary


class TestJsonGeneratedFromSpreadsheet(unittest.TestCase):
    def setUp(self):
        self.data = [['foo', 'bar', 'zap'], [1, 2, 3], [4, 5, 6]]
        self.config = {
            "doc_name": {
                "credentials": "{}",
                "key": "_",
                "worksheet": "sheet1"
            }
        }

    @patch("collector.spreadsheet_to_dictionary.get_google_spreadsheet_data")
    def test_it_returns_a_spreadsheet_as_a_dict(self, mock_spreadsheet_data):
        # Write out a temporary config file somewhere on disk
        f = tempfile.NamedTemporaryFile(suffix=".json")
        f.write(json.dumps(self.config))
        f.flush()

        mock_spreadsheet_data.return_value = self.data

        processed_array = spreadsheet_to_dictionary(['doc_name', f.name])

        expected_array = [
            {'foo': 1, 'bar': 2, 'zap': 3},
            {'foo': 4, 'bar': 5, 'zap': 6},
        ]

        self.assertEqual(processed_array, expected_array)
