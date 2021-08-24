"""
Purpose: To transform and normalize date data.

Author : Albert Ulysses <albertulysseschavez@gmail.com>
"""


def format_date(date: str) -> str:
    """
    Formats the date columns into a common stanard.

    :param date: a datetime or date.
    """
    # TODO: there is probably a nicer way to do this, with better coverage.
    if '/' in date:
        month, day, year = date.split('/')
        if len(day) == 1:
            day = '0{0}'.format(day)
        if len(month) == 1:
            month = '0{0}'.format(month)
        return '{0}-{1}-{2}'.format(year, month, day)
    return date.strip(" []'")[:10]
