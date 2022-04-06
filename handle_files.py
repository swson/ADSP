"""This file contains all the functions that are used to parse a
file into a list and write pandas series to different file format """
import sys

import numpy as np
import pandas as pd
from netCDF4 import Dataset


def read_binary_file(file, data_type):
    """parse the content inside the bin file
    input:  file name of the file to be read
            data type to accommodate 64-bit and 32-bit files
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


def read_nc_file(file, variable):
    """parse the content inside the nc file
    input:  file name of the file to be read
            data type for consistence with read_binary_file
    output: list
            dimension
    """
    data_var = Dataset(file, "r").variables[variable][:]

    return data_var.flatten(), data_var.shape


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


def write_nc_file(series, org_file, file, var, shape):
    """
    write the content of pandas series to a nc file
    nc file will be written in NETCDF4 format
    unlike other write file functions, nc files have metadata within the file and thus
    need to copy other data from the original file too
    method of copying is from
    https://stackoverflow.com/questions/15141563/python-netcdf-making-a-copy-of-all-variables-and-attributes-but-one
    """

    with Dataset(org_file) as src, Dataset(file, "w") as dst:
        # copy global attributes all at once via dictionary
        dst.setncatts(src.__dict__)
        # copy dimensions
        for name, dimension in src.dimensions.items():
            dst.createDimension(
                name, (len(dimension) if not dimension.isunlimited() else None))
        # copy all file data except for the excluded
        for name, variable in src.variables.items():
            if name == var:
                dst.createVariable(name, variable.datatype, variable.dimensions)
                dst[name][:] = np.reshape(series.tolist(), shape)
                # copy variable attributes all at once via dictionary
                dst[name].setncatts(src[name].__dict__)
            else:
                dst.createVariable(name, variable.datatype, variable.dimensions)
                dst[name][:] = src[name][:]
                # copy variable attributes all at once via dictionary
                dst[name].setncatts(src[name].__dict__)
    return
