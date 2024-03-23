"""
Some functions for fetching data from https://data.binance.vision.

Daily download url example: https://data.binance.vision/data/spot/daily/klines/BTCUSDT/1m/BTCUSDT-1m-2023-08-20.zip (contains ohlc data of one day)
Monthly download url example: https://data.binance.vision/data/spot/monthly/klines/BTCUSDT/1m/BTCUSDT-1m-2023-07.zip (contains ohlc data of one month)

Format of the downloaded data: (unix in ms, open, high, low, close, Volume in BTC, ...)
"""

import requests
import calendar
from datetime_utils import check_date_validity

main_url_daily = 'https://data.binance.vision/data/spot/daily/klines/'
main_url_monthly = 'https://data.binance.vision/data/spot/monthly/klines/'
available_time_frames = ['12h', '15m', '1d', '1h', '1m', '1s', '2h', '30m', '3m', '4h', '5m', '6h', '8h']


def date_to_stirng(yy: int, mm: int, dd: int):
    """
    Converts a date from int to string (for generating valid urls).
    if mm < 10 or dd < 10 -> adds 0 before number (e.g., int(8) -> str('08')).
    dd can also be None.
    
    Args:
        yy (int)
        mm (int)
        yy (int)
    Retruns:
        s_yy (str)
        s_mm (str)
        s_yy (str)
    """
    if dd == None:
        date_validity = check_date_validity(yy, mm, 1)
    else:
        date_validity = check_date_validity(yy, mm, dd)
    
    if date_validity:
        s_yy = str(yy)

        if mm < 10:
            s_mm = '0' + str(mm)
        else:
            s_mm = str(mm)

        if dd != None:
            if dd < 10:
                s_dd = '0' + str(dd)
            else:
                s_dd = str(dd)
        else:
            s_dd = None

        return s_yy, s_mm, s_dd
    else:
        raise Exception('Error: Date is not valid.')


def generate_url_and_file_name(asset_pair: str, time_frame: str, yy: int, mm: int, dd: int) -> str:
    """
    This function generates a monthly download url if the :param dd equals None. If :param dd equals to an integer
    it generates a daily download url.

    Args:
        asset_pair (str): e.g., 'BTCUSDT'
        time_frame (str): e.g., '1m' (which stands for 1 minute ohlc candles)
        yy (int)
        mm (int)
        yy (int)
    Returns:
        str: url (e.g., https://data.binance.vision/data/spot/daily/klines/BTCUSDT/1m/BTCUSDT-1m-2023-08-20.zip)
        str: file_name (e.g., 'BTCUSDT-1m-2023-08-20.zip')
    """
    yy, mm, dd = date_to_stirng(yy, mm, dd)
    if dd == None:
        url = main_url_monthly
        file_name = asset_pair + '-' + time_frame + '-' + yy + '-' + mm + '.zip'
    else:
        url = main_url_daily
        file_name = asset_pair + '-' + time_frame + '-' + yy + '-' + mm + '-' + dd + '.zip'

    url += asset_pair + '/' + time_frame + '/' + asset_pair + '-' + time_frame + '-' + yy + '-' + mm

    if dd == None:
        url += '.zip'
    else:
        url += '-' + dd + '.zip'

    return url, file_name


def download_file(url: str, download_path: str) -> None:
    """
    Downloads and saves a file in :param download_path given a :param url.

    Args:
        url (str)
        download_path (str)
    Returns:
        None
    """
    response = requests.get(url)
    if response.status_code == 200:
        # saveing the file:
        file = open(download_path, 'wb')
        file.write(response.content)
        file.close
    else:
        raise Exception(url + ' got HTTP status code ' + str(response.status_code) + '. Binance has not yet updated their dataset. Try again in a couple of hours.')



def download_range_days(asset_pair: str, time_frame: str, 
                        yy_start: int, mm_start: int, dd_start: int, 
                        yy_last: int, mm_last: int, dd_last: int, 
                        folder_path: str):
    """
    Downloads all of the availabe data in a range of days (from start date to last date, including both).
    The data will get downloaded day by day (no monthly data will get downloaded).
    Note: If you want to download a range that is over some months use the download_range_months() function and not this function.

    Args:
        asset_pair (str): e.g., 'BTCUSDT'
        time_frame (str): e.g., '1m' (which stands for 1 minute ohlc candles)
        yy_start (int)
        mm_start (int)
        dd_start (int)
        yy_last (int)
        mm_last (int)
        dd_last (int)
        folder_path (str)
    Returns:
        None
    """
    if not check_date_validity(yy_start, mm_start, dd_start) or not check_date_validity(yy_last, mm_last, dd_last):
        raise Exception('Error: Date is not valid.')
   
    start_date: list[int] = [yy_start, mm_start, dd_start]
    last_date: list[int] = [yy_last, mm_last, dd_last]

    # check if last_date > start_date:
    if last_date[0] <= start_date[0]:
        if last_date[0] < start_date[0]:
            raise Exception('Error: last date is older than start date.')
        if last_date[1] <= start_date[1]:
            if last_date[1] < start_date[1]:
                raise Exception('Error: last date is older than start date.')
            if last_date[2] < start_date[2]:
                raise Exception('Error: last date is older than start date.')
    
    days_to_download: list[list[int]] = [] # [[yy, mm, dd]]
    
    # find the days in the range (between and including start and last):
    date: list[int] = start_date
    last_date_reached = False
    while not last_date_reached:
        # get number of days in month:
        last_day_of_month = calendar.monthrange(date[0], date[1])[1]
        while date[2] <= last_day_of_month:
            days_to_download.append([date[0], date[1], date[2]])
            if last_date == date:
                last_date_reached = True
                break
            date[2] += 1
        date[2] = 1
        date[1] += 1
        if date[1] > 12:
            date[1] = 1
            date[0] += 1
    
    # create url and download data per day:
    for date in days_to_download:
        url, file_name = generate_url_and_file_name(asset_pair, time_frame, date[0], date[1], date[2])
        path = folder_path + '/' + file_name
        download_file(url, path)


def download_range_months(asset_pair: str, time_frame: str, 
                          yy_start: int, mm_start: int,
                          yy_last: int, mm_last: int, 
                          folder_path: str):
    """
    Downloads all of the availabe data in a range of months (from start date to last date, including both).
    The data will get downloaded month by month (not daily).

    Args:
        asset_pair (str): e.g., 'BTCUSDT'
        time_frame (str): e.g., '1m' (which stands for 1 minute ohlc candles)
        yy_start (int)
        mm_start (int)
        yy_last (int)
        mm_last (int)
        folder_path (str)
    Returns:
        None
    """
    if not check_date_validity(yy_start, mm_start, 1) or not check_date_validity(yy_last, mm_last, 1):
        raise Exception('Error: Date is not valid.')
   
    start_date: list[int] = [yy_start, mm_start]
    last_date: list[int] = [yy_last, mm_last]

    # check if last_date > start_date:
    if last_date[0] <= start_date[0]:
        if last_date[0] < start_date[0]:
            raise Exception('Error: last date is older than start date.')
        if last_date[1] < start_date[1]:
            raise Exception('Error: last date is older than start date.')
            
    
    months_to_download: list[list[int]] = [] # [[yy, mm]]
    
    # find the days in the range (between and including start and last):
    date: list[int] = start_date
    last_date_reached = False
    while not last_date_reached:
        while date[1] <= 12:
            months_to_download.append([date[0], date[1]])
            if last_date == date:
                last_date_reached = True
                break
            date[1] += 1
        date[1] = 1
        date[0] += 1
    
    # create url and download data per day:
    for date in months_to_download:
        url, file_name = generate_url_and_file_name(asset_pair, time_frame, date[0], date[1], None)
        path = folder_path + '/' + file_name
        download_file(url, path)
