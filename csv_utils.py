import os
import pandas as pd

def get_lastline(file_path: str) -> str:
    """
    Gets the last line of a file (generally csv files) and returns as a string.
    This function is very useful for large files because it does not read the whole file file (very efficient).

    Here is how it works in a nutshell: 
    The file reader is moved at the very last character of the file. 
    Then the reader jumps backward character by character until it reaches the beginning of the last line. 
    Then it reads the last line into memory.

    Reference: https://www.codingem.com/how-to-read-the-last-line-of-a-file-in-python/

    Args:
        file_path (str)
    Return:
        (str): the last line of the (csv) file in string

    """
    with open(file_path, "rb") as file:
        try:
            file.seek(-2, os.SEEK_END)
            while file.read(1) != b'\n':
                file.seek(-2, os.SEEK_CUR)
        except OSError:
            file.seek(0)
        last_line = file.readline().decode() 
    return last_line


def concat_files(files: list[str]) -> None:
    """
    This function concatenates csv files together.
    All files (except the first file) will get concatenated to the first file of the :param files list.
    The order of the concatenation is as the order of the paths of the files in the :param files list.
    E.g., files = [f1.csv, f2.csv, f3.csv] --> concat_files(files) --> f1.csv = f1.csv + f2.csv + f3.csv 

    Args:
        files (list[str]): list of the paths of the input csv files
    Returns:
        None
    """
    add_newline = False
    first_file_last_line = get_lastline(files[0])
    if list(first_file_last_line)[-1] != '\n':
        add_newline = True

    first_file = open(files[0], 'a')
    if add_newline:
        first_file.write('\n')

    for i in range(1, len(files)):
        file = open(files[i], 'r')
        file_lines = file.readlines()
        for line in file_lines:
            first_file.write(line)
        file.close()
    first_file.close()
    
    print('Files appended together.')


def delete_files(files: list[str]) -> None:
    """
    A function for deleting files from the compter.
    Deletes the files, based on the file paths in the :param files list.

    Args:
        files (list[str]): list of the paths of the files
    Returns:
        None
    """
    for i in range(len(files)):
        os.remove(files[i])
    print('Files deleted.')
