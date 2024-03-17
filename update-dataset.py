import os
import shutil
import argparse
from fetch_data import download_range_days
from reformat_data import reformat_binance_vision_kline_files
from csv_utils import get_lastline, concat_files
from datetime_utils import timestamp_to_UTC, get_next_day_date, get_previous_day_date, get_today_date

dataset_PATH: str = './dataset-5m.csv'


def update_my_btcusdt_data(time_frame: str, PATH_Binance_spot_BTCUSDT_Xm: str) -> None:
    """
    This function downloads binance spot BTCUSDT (time_frame: 1m or 5m) data, reformats it, 
    and appends it to PATH_Binance_spot_BTCUSDT_Xm.
    This function downloads daily data (day by day not monthly).
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
    print('Downloading the data...')
    download_range_days('BTCUSDT', time_frame, yy_start, mm_start, dd_start, yy_last, mm_last, dd_last, './output')
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
