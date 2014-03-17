import string


def sanitise_string(messy_str):
    """Whitelist characters in a string"""
    valid_chars = ' {0}{1}'.format(string.ascii_letters, string.digits)
    return u''.join(char for char in messy_str if char in valid_chars).strip()


class Service(object):
    def __init__(self, numeric_id, detailed_data):
        self.numeric_id = numeric_id
        self.detailed_data = detailed_data

    def identifier(self):
        """Return a unique identifier for the service"""
        # TODO: How do we uniquely identify a service?
        service_title = self.service_title()
        dept = self.abbreviated_department()
        return sanitise_string(u'{0} {1} {2}'.format(self.numeric_id, dept, service_title))

    def get(self, key):
        return self.detailed_data[key]

    def service_title(self):
        return self.get('Name of service')

    def abbreviated_department(self):
        return self.get('Abbr')
