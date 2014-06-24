# -*- coding: utf-8 -*-
import string


def sanitise_string(messy_str):
    """Whitelist characters in a string"""
    valid_chars = ' {0}{1}'.format(string.ascii_letters, string.digits)
    return u''.join(char for char in messy_str if char in valid_chars).strip()


class Service(object):
    def __init__(self, numeric_id, detailed_data):
        self.numeric_id = numeric_id
        self.detailed_data = detailed_data

    def attribute_exists(self, key):
        return key in self.detailed_data

    def get_datum(self, key):
        datum = self.handle_bad_data(self.get(key))
        return datum

    def get(self, key):
        return self.detailed_data[key]

    def identifier(self):
        """Return a unique identifier for the service"""
        return self.get('Slug')

    def service_title(self):
        return self.get('Name of service')

    def abbreviated_department(self):
        return self.get('Abbr')

    def handle_bad_data(self, datum):
        # TODO: Should we be more explicit about non-requested (***) data?
        if datum == '' or datum == '-' or datum == '***' or datum == None:
            return None
        elif not isinstance(datum, (int, long, float, complex)):
            # If the value we get from the spreadsheet is not numeric, send
            # that to Backdrop as a null data point
            print "Data from the spreadsheet doesn't look numeric: <{0}> (from {1})".format(datum, self.identifier())
            return None
        else:
            return datum
