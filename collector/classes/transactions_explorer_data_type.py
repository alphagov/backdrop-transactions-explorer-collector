class TransactionsExplorerDataType(object):
    """Represents a type of data that is stored in Transactions Explorer"""
    def __init__(self, title, key_format, metrics, periods, period_duration):
        self.title = title
        self.key_format = key_format
        self.metrics = metrics
        self.periods = periods
        self.period_duration = period_duration

    def get_key(self, metric, period):
        """Returns the row title (key) based on the format used"""
        key = self.key_format
        key = key.replace('{metric}', metric)
        key = key.replace('{period}', period)
        return key

    def get_period_start_date(self, period_key):
        return self.periods[period_key]['_start_at']

    def get_period_end_date(self, period_key):
        return self.periods[period_key]['_end_at']
