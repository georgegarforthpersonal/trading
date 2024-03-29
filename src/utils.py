from datetime import datetime


def get_datetime_from_oanda_datetime_str(datetime_str):
    """Oanda datetime strings are in the format '2022-01-01T00:00:00.000000000Z'"""
    return datetime.strptime(datetime_str.split('.')[0], '%Y-%m-%dT%H:%M:%S')