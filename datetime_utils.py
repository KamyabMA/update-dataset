import datetime

def check_date_validity(yy: int, mm: int, dd: int) -> bool:
    """
    This function checks if a given date is valid and if it actually exist.

    Args:
        yy (int): year
        mm (int): month
        dd (int): day
    Returns:
        bool: True if date is valid else False.
    """
    try:
        datetime.datetime(year=yy,month=mm,day=dd)
        return True
    except ValueError:
        return False
    

def timestamp_to_UTC(timestamp_in_s):
    """
    Converts a timestamp in seconds to UTC datetime.
    Code example of how to use this function:
    yy, mm, dd, hour, min, sec =  timestamp_to_UTC(1692489540)

    Args:
        timestamp: (int or float)
    Returns:
        year, month, day, hour, minute, second (all in int)
    """
    dt = datetime.datetime.utcfromtimestamp(timestamp_in_s)
    return dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second


def timestamp_to_utc_datetime(timestamp_in_s) -> datetime.datetime:
    """
    Converts a timestamp in seconds to UTC datetime.datetime object.
    Code example of how to use this function:
    date =  timestamp_to_utc_datetime(1692489540)

    Args:
        timestamp: (int or float)
    Returns:
        date (datetime)
    """
    dt = datetime.datetime.utcfromtimestamp(timestamp_in_s)
    return dt


def get_next_day_date(yy: int, mm: int, dd: int):
    """
    Gets the next day in calender.
    Code example of how to use this function:
    yy, mm, dd =  get_next_day_date(2023, 2, 28)

    Args:
        yy (int)
        mm (int)
        dd (int)
    Returns:
        yy, mm, dd (all in int)
    """
    dt = datetime.datetime(year=yy, month=mm, day=dd)
    dt = dt + datetime.timedelta(days=1)
    return dt.year, dt.month, dt.day


def get_previous_day_date(yy: int, mm: int, dd: int):
    """
    Gets the previous day in calender.
    Code example of how to use this function:
    yy, mm, dd =  get_previous_day_date(2023, 2, 28)

    Args:
        yy (int)
        mm (int)
        dd (int)
    Returns:
        yy, mm, dd (all in int)
    """
    dt = datetime.datetime(year=yy, month=mm, day=dd)
    dt = dt - datetime.timedelta(days=1)
    return dt.year, dt.month, dt.day


def get_today_date():
    """
    Gets the date of the current day.
    Code example of how to use this function:
    yy, mm, dd =  get_today_date()

    Args:
        -
    Returns:
        yy, mm, dd (all in int)
    """
    dt = datetime.datetime.today()
    return dt.year, dt.month, dt.day

def get_last_day_of_month(yy: int, mm: int):
    """
    Gets the date of the last day of a given month.
    Code example of how to use this function:
    yy, mm, dd =  get_last_day_of_month(2023, 2)

    Args:
        yy (int)
        mm (int)
    Returns:
        yy, mm, dd (all in int)
    """
    # get first date of the next month:
    if mm == 12:
        dt = datetime.datetime(year=yy+1, month=1, day=1)
    else:
        dt = datetime.datetime(year=yy, month=mm+1, day=1)
    # return the previuos date as the last day of the current month:
    return get_previous_day_date(dt.year, dt.month, dt.day)
