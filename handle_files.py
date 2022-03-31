"""This file contains all the functions that are used to parse a
file into a list and write pandas series to different file format """
import sys

import numpy as np
import pandas as pd


def read_binary_file(file, data_type):
    """parse the content inside the bin file
    input:  file name of the file to be read
            data type of the binary file
    output: list"""

    if data_type == 'f':
        # parse little-endian 64 bit floating point
        return np.fromfile(file, '<f8').tolist()
    elif data_type == 's':
        # parse little-endian 32 bit floating point
        return np.fromfile(file, '<f4').tolist()
    else:
        sys.stderr.write("ERROR: invalid data type at read_binary_file\n")

def read_csv_file(file, data_type):
    """parse the content inside the csv file
    input:  file name of the file to be read
            data type for consistence with read_binary_file
    output: list"""

    series = pd.read_csv(file, header=None).squeeze("columns")

    return series.values.tolist()


def read_nc_file(file, header):
    return


def write_binary_file(series, file, data_type):
    """write the content of pandas series to a bin file"""

    if data_type == 'f':
        # format is little-endian 64 bit floating point
        series.to_numpy(dtype='<f8').tofile(file)
    elif data_type == 's':
        # format is little-endian 32 bit floating point
        series.to_numpy(dtype='<f4').tofile(file)
    else:
        sys.stderr.write("ERROR: invalid data type at write_binary_file\n")

    return


def write_csv_file(series, file, data_type):
    """write the content of pandas series to a csv file"""

    series.to_csv(file, header=None, index=None)

    return
