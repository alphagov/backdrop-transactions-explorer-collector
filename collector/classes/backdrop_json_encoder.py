import datetime
import json


class BackdropJSONEncoder(json.JSONEncoder):
    """Class to serialise JSON with timestamps that Backdrop likes"""
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%S+00:00')

        return json.JSONEncoder.default(self, obj)
