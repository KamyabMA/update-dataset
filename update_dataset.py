import os
import shutil
import datetime
import argparse
from fetch_data import download_range_days, download_range_months
from reformat_data import reformat_binance_vision_kline_files
from csv_utils import get_lastline, concat_files
from datetime_utils import timestamp_to_UTC, get_next_day_date, get_previous_day_date, get_today_date, get_last_day_of_month

dataset_PATH: str = './dataset-5m.csv'

def get_download_plan(yy_start: int, mm_start: int, dd_start: int, 
                      yy_last: int, mm_last: int, dd_last: int):
    """
    Depending on the start date (given by yy_start, mm_start, dd_start) and the last date given by
    (yy_last, mm_last, dd_last), this function calculates the days and months that should be downloaded.

    Args:
        yy_start (int)
        mm_start (int)
        dd_start (int)
        yy_last (int)
        mm_last (int)
        dd_last (int)
    Returns:
        [dict] (list of dicts)
        dict: {
            'data_type' = 'd' or 'm'
            'start_date' = [yy, mm, dd] or [yy, mm]
            'end_date' = [yy, mm, dd] or []
        }
    """
    start_date = datetime.datetime(yy_start, mm_start, dd_start)
    end_date = datetime.datetime(yy_last, mm_last, dd_last)
    if start_date < end_date:
        download_plan = []
        temp_date = start_date - datetime.timedelta(days=1) # gets the date before start date
        while temp_date != end_date:
            temp_date = temp_date + datetime.timedelta(days=1) # gets next day date 
            _, _, temp_date_ldm =  get_last_day_of_month(temp_date.year, temp_date.month)
            if temp_date.day == 1 and (datetime.datetime(temp_date.year, temp_date.month, temp_date_ldm) < end_date or 
                                    datetime.datetime(temp_date.year, temp_date.month, temp_date_ldm) == end_date):
                download_plan.append({
                    'data_type' : 'm',
                    'start_date' : [temp_date.year, temp_date.month],
                    'end_date' : []
                })
                temp_date = datetime.datetime(temp_date.year, temp_date.month, temp_date_ldm)
            elif temp_date.year == end_date.year and temp_date.month == end_date.month:
                download_plan.append({
                    'data_type' : 'd',
                    'start_date' : [temp_date.year, temp_date.month, temp_date.day],
                    'end_date' : [end_date.year, end_date.month, end_date.day]
                })
                temp_date = end_date
            else:
                download_plan.append({
                    'data_type' : 'd',
                    'start_date' : [temp_date.year, temp_date.month, temp_date.day],
                    'end_date' : [temp_date.year, temp_date.month, temp_date_ldm]
                })
                temp_date = datetime.datetime(temp_date.year, temp_date.month, temp_date_ldm)
        
        return download_plan
    else:
        raise Exception('start_date >= last_date')


def update_my_btcusdt_data(time_frame: str, PATH_Binance_spot_BTCUSDT_Xm: str) -> None:
    """
    This function downloads binance spot BTCUSDT (time_frame: 1m or 5m) data, reformats it, 
    and appends it to PATH_Binance_spot_BTCUSDT_Xm.
    It looks what is the last row of PATH_Binance_spot_BTCUSDT_Xm, and downloads all the data
    until the last available daily historic data of https://data.binance.vision.

    Args:
        time_frame (str): ['1m', '5m']
        PATH_Binance_spot_BTCUSDT_Xm (str)
    Returns:
        None
    """
    if not os.path.exists('./output'):
        os.mkdir('./output')

    # get the last timestamp of PATH_Binance_spot_BTCUSDT_Xm to figure out the data range, that is needed to download:
    last_timestamp = get_lastline(PATH_Binance_spot_BTCUSDT_Xm).split(',')[0]
    yy, mm, dd, _, _, _ =  timestamp_to_UTC(int(last_timestamp))

    # get next day in calender:
    yy_start, mm_start, dd_start =  get_next_day_date(yy, mm, dd)

    # get the end date of the download range (the day before today):
    yy_today, mm_today, dd_today = get_today_date()
    yy_last, mm_last, dd_last = get_previous_day_date(yy_today, mm_today, dd_today)

    if yy == yy_last and mm == mm_last and dd == dd_last:
        raise Exception(f'Dataset {str(PATH_Binance_spot_BTCUSDT_Xm)} is already up to date.')

    # download and reformat the data:
    print("Downloading data...")
    download_plan = get_download_plan(yy_start, mm_start, dd_start, yy_last, mm_last, dd_last)
    try:
        for dict in download_plan:
            if dict['data_type'] == 'd':
                yy_start = dict['start_date'][0]
                mm_start = dict['start_date'][1]
                dd_start = dict['start_date'][2]
                yy_last = dict['end_date'][0]
                mm_last = dict['end_date'][1]
                dd_last = dict['end_date'][2]
                download_range_days('BTCUSDT', time_frame, yy_start, mm_start, dd_start, yy_last, mm_last, dd_last, './output')
            else:
                # dict['data_type'] = 'm'
                yy_start = dict['start_date'][0]
                mm_start = dict['start_date'][1]
                yy_last = yy_start
                mm_last = mm_start
                download_range_months('BTCUSDT', time_frame, yy_start, mm_start, yy_last, mm_last, './output')
    except:
        pass
    print('Download completed.')
    reformat_binance_vision_kline_files('./output', './output/new_data.csv')

    # concat the data to PATH_Binance_spot_BTCUSDT_Xm:
    concat_files([PATH_Binance_spot_BTCUSDT_Xm, './output/new_data.csv'])

    os.remove('./output/new_data.csv')
    shutil.rmtree('./output')
    print(f'New data appended to {str(PATH_Binance_spot_BTCUSDT_Xm)}.')
    print(f'Dataset {str(PATH_Binance_spot_BTCUSDT_Xm)} is now up to date.')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-update','--update_dataset', action="store_true", help="Updates Binance spot BTCUSDT 1m and 5m datasets.")

    args = parser.parse_args()
    
    if args.update_dataset:
        update_my_btcusdt_data('5m', dataset_PATH)
