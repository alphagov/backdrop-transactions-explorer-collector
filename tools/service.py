from decimal import Decimal
from functools import total_ordering
import re
import itertools
from datetime import date
from dateutil.relativedelta import relativedelta
from helper import keyify, as_number


class Service:
    EXPECTED_QUARTERS = [
        # worked through oldest to newest to calculate %age changes
        '2012_q4',
        '2013_q1',
        '2013_q2',
        '2013_q3',
        '2013_q4',
        '2014_q1',
        '2014_q2',
        '2014_q3',
    ]
    COVERAGE_ATTRIBUTES = ['vol', 'digital_vol', 'cpt']

    # A marker used in the spreadsheet to show that a metric was not requested
    NOT_REQUESTED_MARKER = '***'

    def __init__(self, details):
        for key in details:
            setattr(self, keyify(key), details[key])
        self.has_kpis = False
        self.calculate_quarterly_kpis()
        self.keywords = self._split_keywords(details)

    def calculate_quarterly_kpis(self):
        self.kpis = []
        previous_quarter = None
        self.has_previous_quarter = False

        for quarter in self.EXPECTED_QUARTERS:
            volume = as_number(self['%s_vol' % quarter])
            if volume is None:
                continue

            digital_volume = as_number(self['%s_digital_vol' % quarter])
            if digital_volume == 0:
                takeup = 0
            elif digital_volume is not None and volume is not None:
                takeup = digital_volume / volume
            else:
                takeup = None

            cost_per_transaction = as_number(self['%s_cpt' % quarter])

            if cost_per_transaction is not None:
                cost = cost_per_transaction * volume
            else:
                cost = None

            data = {
                'quarter':          Quarter.parse(quarter),
                'takeup':           takeup,
                'cost':             cost,
                'volume':           self['%s_vol' % quarter],
                'volume_num':       volume,
                'digital_volume':   self['%s_digital_vol' % quarter],
                'digital_volume_num': digital_volume,
                'cost_per':         self['%s_cpt' % quarter],
                'cost_per_number':  cost_per_transaction,
                'cost_per_digital': self['%s_digital_cpt' % quarter],
                'completion':       self['%s_completion_rate' % quarter],
                'satisfaction':     self['%s_user_satisfaction' % quarter],
            }

            def change_factor(previous, current):
                factor = None
                if current is not None and previous is not None and previous != 0:
                    factor = current / previous
                return factor

            if previous_quarter is not None:
                self.has_previous_quarter = True
                data['volume_change'] = change_factor(previous_quarter['volume_num'], volume)
                data['takeup_change'] = change_factor(previous_quarter['takeup'], takeup)
                data['cost_per_change'] = change_factor(previous_quarter['cost_per_number'], cost_per_transaction)
                data['cost_change'] = change_factor(previous_quarter['cost'], cost)
                data['previous_quarter'] = previous_quarter['quarter']

            previous_quarter = data
            self.kpis.append(data)
            self.has_kpis = True

    @property
    def name(self):
        return re.sub('\s*$', '', self.name_of_service)

    @property
    def body(self):
        return self.agency_body

    @property
    def agency_abbreviation(self):
        if self.agency_abbr is None or len(self.agency_abbr) == 0:
            return self.body
        else:
            return self.agency_abbr

    @property
    def description(self):
        return re.sub('\s*$', '', self.description_of_service)

    def latest_kpi_for(self, attribute):
        latest_kpis = self._most_recent_kpis
        if latest_kpis is None:
            return None
        else:
            return latest_kpis.get(attribute)

    @property
    def _most_recent_kpis(self):
        if len(self.kpis) > 0:
            return self.kpis[-1]

    @property
    def data_coverage(self):
        def is_requested(attr):
            return str(self[attr]).lower() != self.NOT_REQUESTED_MARKER

        def is_provided(attr):
            return as_number(self[attr]) is not None

        all_attrs = map('_'.join, itertools.product(
            self.EXPECTED_QUARTERS, self.COVERAGE_ATTRIBUTES))
        all_requested = filter(is_requested, all_attrs)
        all_provided = filter(is_provided, all_requested)

        return Coverage(len(all_provided), len(all_requested))

    def _attributes_present(self, kpi, attrs):
        return all(kpi[attr] is not None for attr in attrs)

    def find_recent_kpis_with_attributes(self, attrs):
        return next((kpi for kpi in reversed(self.kpis)
                     if self._attributes_present(kpi, attrs)),
                    None)

    @property
    def slug(self):
        return slugify('%s-%s' % (self.abbr, self.name))

    @property
    def link(self):
        return '%s/%s' % ('service-details', self.slug)

    @property
    def has_details_page(self):
        return self.detailed_view == 'yes'

    @property
    def most_up_to_date_volume(self):
        most_recent_yearly_volume = None
        if self.has_kpis:
            most_recent_yearly_volume = self.latest_kpi_for('volume_num')
        return most_recent_yearly_volume

    def historical_data_before(self, quarter, key):
        previous_kpis = filter(lambda k: k['quarter'] < quarter, self.kpis)

        if key == 'cost_per_number' or key == 'cost':
            # Don't return cost_per_number or cost if cost_per_number is not provided
            previous_kpis = [elem for elem in previous_kpis if elem['cost_per_number'] is not None]
        elif key == 'takeup':
            # Don't return takeup value if digital_volume_num is not provided
            previous_kpis = [elem for elem in previous_kpis if elem['digital_volume_num'] is not None]

        key_data = lambda k: {'quarter': k['quarter'], 'value': k.get(key)}
        return map(key_data, reversed(previous_kpis))

    def __getitem__(self, key):
        return getattr(self, key)

    def _split_keywords(self, details):
        if not details['Keywords']:
            return []
        return [x.strip() for x in details['Keywords'].split(',')]


@total_ordering
class Quarter:
    def __init__(self, year, quarter):
        self.year = year
        self.quarter = quarter

    def __str__(self):
        if self.year == 2012 and self.quarter == 4:
            # Exception for Q4 2012
            return "%s to %s" % (self.format_date(date(2011, 4, 1)), self.format_date(date(2012, 3, 1)))

        q = self.quarter * 3
        end_date = date(self.year, q, 1) - relativedelta(months=3)
        start_date = end_date - relativedelta(months=11)
        return "%s to %s" % (self.format_date(start_date), self.format_date(end_date))

    def __lt__(self, quarter):
        return (self.year, self.quarter) < (quarter.year, quarter.quarter)

    def __eq__(self, quarter):
        return (self.year, self.quarter) == (quarter.year, quarter.quarter)

    def __repr__(self):
        return '<Quarter year=%s quarter=%s>' % (self.year, self.quarter)

    month_abbreviations = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'June',
        'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'
    ]

    @classmethod
    def format_date(cls, date):
        return "%s %s" % (cls.month_abbreviations[date.month - 1], date.strftime('%Y'))

    @classmethod
    def parse(cls, str):
        m = re.match('(\d\d\d\d)_q(\d)', str)
        return Quarter(int(m.group(1)), int(m.group(2)))


class Coverage(object):
    def __init__(self, provided, requested):
        self.provided = provided
        self.requested = requested

    @property
    def percentage(self):
        return Decimal(self.provided) / Decimal(self.requested)

    def __add__(self, other):
        return Coverage(self.provided + other.provided, self.requested + other.requested)
