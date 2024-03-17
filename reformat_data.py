"""
Some functions for editing (reformating) the format of the price data downloaded from https://data.binance.vision.
"""

import os
import re
from zipfile import ZipFile
import pandas as pd

def reformat_binance_vision_kline_files(folder_path: str, output_path: str):
    """
    This function converts binance.vision spot kline price data zip files with the format
    (unix in ms, open, high, low, close, Volume in BTC, ...) into csv files with the fromat
    (unix in seconds, open, hich, low, close).
    It deletes the original zip files after reformatig each zip file.
    All reformated data will be stored in a single csv file (:param output_path).
    Note: This function will try to reformat all the '.zip' files in the directory :param folder_path.
          So it will not work properly if other types of '.zip' files are contained in :param folder_path. 
    Best practice: Create a folder only containing the zip files that you want to reformat and pass the
                   the path of this folder.

    Args:
        folder_path (str): path of the folder containing the zip files
        output_path (str): path should contain .csv at the end (to make it actually a csv file)
    Returns:
        None
    """
    # creating a csv file to save the reformated data in it:
    result_csv_file = open(output_path, 'w')
    result_csv_file.close()

    # getting the '.zip' files in the :param folder_path directory:
    zip_files: list[str] = []
    dir_ls = os.listdir(folder_path)
    for file in dir_ls:
        if re.findall('.zip', file) != []:
            zip_files.append(file)
    zip_files.sort()
    
    # opening each '.zip' file and reformating and saving the kline data:
    for file in zip_files:
        csv_name = file.replace('.zip', '.csv')
        with ZipFile(folder_path + '/' + file, 'r') as zip: # opening the zip file in READ mode
            zip.extract(csv_name) # extracting the csv file from the zip file
        df = pd.read_csv(csv_name, header=None)
        os.remove(csv_name) # deleting the extracted csv file
        
        # reformating:
        df = df.drop(columns=[5, 6, 7, 8, 9, 10, 11])
        ms_to_s = lambda x: x/1000
        df[0] = df[0].apply(ms_to_s)

        # writing (appending) the reformated data to output csv file:
        result_csv_file = open(output_path, 'a')
        for i in range(len(df)):
            reformated_row = str(int(df.iloc[i][0])) + ',' + str(df.iloc[i][1]) + ',' + str(df.iloc[i][2]) + ',' + str(df.iloc[i][3]) + ',' + str(df.iloc[i][4])
            result_csv_file.write(reformated_row + '\n')
        result_csv_file.close()
        os.remove(folder_path + '/' + file)
    print('Data reformated and saved.')