import datetime
import pytz


def tzware_datetime():
    """
    Return a timezone aware datetime.

    :return: Datetime
    """
    return datetime.datetime.now(pytz.utc)


def tzware(date):
    """It takes a datetime object and returns a new datetime object with the timezone set to
    Australia/Melbourne

    Parameters
    ----------
    date
        The date to be converted

    Returns
    -------
        A datetime object with the timezone set to Australia/Melbourne

    """
    return date.astimezone(pytz.utc)
