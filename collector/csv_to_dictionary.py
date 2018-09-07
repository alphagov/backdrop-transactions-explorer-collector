# -*- coding: utf-8 -*-
import unicodecsv


def csv_to_dictionary(path):
    with open(path, 'r') as services_csv:
        reader = unicodecsv.reader(services_csv)
        return _convert_to_records(reader)


def _convert_to_records(iterable):
    records = []
    header_row = []
    for row in iterable:
        if not header_row:
            for header in row:
                header_row.append(_tidy_header(header))
        else:
            tidied_row = []
            for cell in row:
                tidied_row.append(_process_cell(cell))
            records.append(dict(zip(header_row, tidied_row)))
    return records


def _process_cell(s):
    try:
        return int(s)
    except (ValueError, TypeError):
        try:
            return float(s)
        except (ValueError, TypeError):
            return s


def _tidy_header(header):
    """Removes pound signs from the end of
       Transactions Explorer headers, because string encoding
       is never fun"""
    return header.replace(u'(£)', '').strip()
