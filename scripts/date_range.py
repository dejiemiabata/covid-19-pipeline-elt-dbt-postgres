from datetime import date, timedelta


# yields each date from start to date, inclusive
def date_range(start: date, end: date):
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)
