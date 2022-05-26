import argparse
import os
import random
import sys
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import rcParams
from prettytable import PrettyTable
from openpyxl.workbook import Workbook

import handle_files
import dct

INPUT_DIR = "data"
OUTPUT_DIR = "result"
ANOMALY_TYPE_LIST = ["point", "collective"]
READ_FILE = {".bin": handle_files.read_binary_file,
             ".dat": handle_files.read_binary_file,
             ".csv": handle_files.read_csv_file,
             ".nc": handle_files.read_nc_file}
WRITE_FILE = {".bin": handle_files.write_binary_file,
              ".dat": handle_files.write_binary_file,
              ".csv": handle_files.write_csv_file,
              ".nc": handle_files.write_nc_file}
plot_flag = False
dct_flag = False
PLOT_WINDOW_SIZE = 100
# specific the energy percentage needed to represent
# the DCT coefficients
ENERGY_PERCENTAGE_LIST = [0.90, 0.95, 0.99, 0.999, 0.9999, 0.99999, 0.999999]


def anomaly_data_generator(error_rate, anomaly_type_num, injection_rate, err_metric,
                           filename, file_extension, data_type, variable):
    """inject errors into the original data file and then output the
    anomaly file along with information on error injection"""

    # nc files are handled differently since they are more complex
    if file_extension == ".nc":
        try:
            original, dimension = READ_FILE[file_extension](filename + file_extension, variable)
        except TypeError:
            # if there is a TypeError, read nc file fails due to problem with variables
            return
    else:
        original = READ_FILE[file_extension](filename + file_extension, data_type)

    anomaly_type = ANOMALY_TYPE_LIST[anomaly_type_num]
    output_file = output_file_name(OUTPUT_DIR, filename, err_metric, error_rate, injection_rate, file_extension)
    data_size = len(original)

    df_org = pd.Series(original)
    df = df_org.copy()

    error_num = int(data_size * injection_rate)
    # get a list of random errors
    error_list = get_error_list(anomaly_type, data_size, error_num)
    error_list.sort()

    print("--------------------------------------------")
    print("input filename:    " + filename + file_extension)
    print("output filename:   " + output_file)
    print("time:              " + time.asctime(time.localtime()))
    print("error type:        " + anomaly_type)
    print("error metrics:     " + err_metric)
    print(f"data size:         {data_size:d}")
    print(f"Number of errors:  {error_num:d}")
    print(f"Error list:\n{*error_list,}")

    if error_num == 0:
        print("WARNING: Injection rate is too low, no errors is injected, an error injected file will not be created")
        print("--------------------------------------------")

        return

    if err_metric == "relative":
        print("max point:", df_org.max(0), "min point:", df_org.min(0))
        err_para = (df_org.max(0) - df_org.min(0)) * error_rate
    else:
        err_para = error_rate

    table = PrettyTable(["Error Number", "Location", "Original Value", "New Injected Value"])
    table.align = "r"
    for error_num, error_index in enumerate(error_list):
        df[error_index] = get_error(df[error_index], err_para, err_metric)
        table.add_row([error_num, error_index, df_org[error_index], df[error_index]])

    # injection detail is not needed for DCT
    if not dct_flag:
        print(table)

    mse = get_mse(df_org.tolist(), df.tolist())
    print("mean square error: ", mse)

    if dct_flag:
        kneel = dct.knee_locator(df_org.tolist())
        print("Knee point is", kneel)
        table = PrettyTable()
        header = ["Original Concentration", "Error Concentration", "Energy Percentage (%)", "Compaction Ratio (%)"]
        table.field_names = header
        table.align = "r"
        df1 = pd.DataFrame(header)

        for energy_percentage in ENERGY_PERCENTAGE_LIST:
            original_energy = dct.get_coefficient(df_org.tolist(), energy_percentage)
            error_energy = dct.get_coefficient(df.tolist(), energy_percentage)
            row_ele = [original_energy, error_energy, energy_percentage * 100, original_energy / df_org.size * 100]
            table.add_row(row_ele)
            df1 = pd.concat([df1, pd.Series(row_ele)], ignore_index=True, axis=1)
        print(table)

        df1 = df1.T
        (path, keyword) = os.path.split(filename)
        try:
            with pd.ExcelWriter(keyword + '_error.xlsx', mode='a') as writer:
                df1.to_excel(writer, sheet_name=str(error_rate)+"_"+str(injection_rate), index=False, header=False)
        except FileNotFoundError:
            with pd.ExcelWriter(keyword + '_error.xlsx', mode='w') as writer:
                df1.to_excel(writer, sheet_name=str(error_rate) + "_" + str(injection_rate), index=False, header=False)

    if file_extension == ".nc":
        WRITE_FILE[file_extension](df, filename + file_extension, output_file, variable, dimension)
    else:
        WRITE_FILE[file_extension](df, output_file, data_type)
    print("--------------------------------------------")

    if plot_flag:
        plot_data(df_org, df, error_list, anomaly_type, filename)

    return


def get_error(cur_val, para, err_metric):
    """return the error injected value
    input:
    cur_val     -   current data value
    para        -   input parameter
    err_metric  -   type of error

    there are three error metric: absolute, relative, and point
    absolute -  return a random floating point number between
                cur_val-para and cur_val+para
    relative -  return a random floating point number between
                cur_val-(max-min)*para and cur_val+(max-min)*para
    point    -  return a random floating point number between
                cur_val-cur_val*para, cur_val+cur_val*para
    gauss    -  return a random floating point number based
                on a Gaussian distribution with a mean of cur_val
                and standard deviation of para
    """
    # print(para)
    if err_metric == "absolute":
        # print("Range from", cur_val - para, "to", cur_val + para)
        return random.uniform(cur_val - para, cur_val + para)
    elif err_metric == "relative":
        # print("Range from", cur_val - para, "to", cur_val + para)
        return random.uniform(cur_val - para, cur_val + para)
    elif err_metric == "point":
        # print("Range from", cur_val * (1 - para), "to", cur_val * (1 + para))
        return random.uniform(cur_val * (1 - para), cur_val * (1 + para))
    elif err_metric == "gauss":
        return random.gauss(cur_val, para)
    else:
        print("ERROR: Invalid error metrics")
        sys.stderr.write("ERROR: Invalid error metrics\n")
        quit()


def get_mse(list_org, list_new):
    """Take in two lists of same length and then
    find the mse between them"""

    arr_org = np.array(list_org)
    arr_new = np.array(list_new)

    mse = np.nanmean(np.square(arr_org - arr_new))

    return mse


def plot_data(org_data, new_data, error_list, anomaly_type, data_name):
    """plot original data and anomaly data together for comparison"""

    new_data = new_data.rename("anomaly")
    org_data = org_data.rename("original")
    # plot the error points one by one
    if new_data.size < PLOT_WINDOW_SIZE:
        print("ERROR: data size too small, must be greater than window size ", PLOT_WINDOW_SIZE * 2, " to plot")
        sys.stderr.write("ERROR: data size too small, must be greater than window size to plot\n")
        exit()
    plt.xlabel("Index")
    plt.ylabel("Value")
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']

    if anomaly_type == "point":
        for count, index in enumerate(error_list):
            plot_start = index - PLOT_WINDOW_SIZE
            plot_end = index + PLOT_WINDOW_SIZE
            if plot_start < 0:
                plot_start = 0
                plot_end = PLOT_WINDOW_SIZE * 2
            if plot_end > new_data.size:
                plot_start = new_data.size - PLOT_WINDOW_SIZE * 2
                plot_end = new_data.size
            ax = new_data[plot_start:plot_end].plot(color='r', linewidth=0.5)
            ax.set_title(data_name + " | Error " + str(count + 1))
            org_data[plot_start:plot_end].plot(ax=ax, linewidth=0.5)

            plt.legend()
            plt.show()
    elif anomaly_type == "collective":
        plot_start = error_list[0] - PLOT_WINDOW_SIZE
        plot_end = error_list[-1] + PLOT_WINDOW_SIZE
        if plot_start < 0:
            plot_start = 0
            plot_end = PLOT_WINDOW_SIZE * 2
        if plot_end > new_data.size:
            plot_start = new_data.size - PLOT_WINDOW_SIZE * 2
            plot_end = new_data.size

        ax = new_data[plot_start:plot_end].plot(color='r', linewidth=0.5)
        ax.set_title(data_name + " | Collective Error")
        org_data[plot_start:plot_end].plot(ax=ax, linewidth=0.5)

        plt.legend()
        plt.show()


def output_file_name(folder_name, file_path, err_metric, error_rate, injection_rate, file_type):
    """create the name of output file"""

    (path, file_name) = os.path.split(file_path)

    error_rate = '%.2f' % error_rate
    injection_rate = '%.2f' % injection_rate
    error_str = str(error_rate).replace(".", "p")
    injection_str = str(injection_rate).replace(".", "p")

    return os.path.join(folder_name, file_name + "_" + err_metric + "_" + error_str + "_" + injection_str + file_type)


def get_error_list(anomaly_type, list_size, error_num):
    """create the list of integers to inject the errors to, the list represents the error index"""
    if anomaly_type == "point":
        # get a non-repeating list of random array index
        error_list = random.sample(range(0, list_size), error_num)
    elif anomaly_type == "collective":
        # get a list of consecutive integers
        collective_mid = random.randrange(0, list_size)

        collective_start = collective_mid - error_num // 2
        collective_start = 0 if collective_start < 0 else collective_start

        collective_end = collective_mid + error_num // 2
        collective_end = list_size if collective_end > list_size else collective_end

        error_list = list(range(collective_start, collective_end))
    else:
        print("ERROR: anomaly_type not recognized")
        return

    return error_list


def test_anomaly_gen_hpcdata(usr_input):
    global OUTPUT_DIR
    global plot_flag
    global dct_flag
    plot_flag = usr_input.plot
    dct_flag = usr_input.dct

    # set output folder if specified by user
    if usr_input.output:
        OUTPUT_DIR = usr_input.output

    if not os.path.isdir(OUTPUT_DIR):
        print("ERROR: \"" + OUTPUT_DIR + "\" folder does not exist, create the folder or "
                                         "specify a different folder")
        quit()

    sys.stdout = open('log.txt', 'w')

    for f in usr_input.file:
        filename, file_extension = os.path.splitext(f)
        if not (READ_FILE.get(file_extension)):
            print("WARNING: " + file_extension + " file type not supported")
            continue

        for t in usr_input.anomaly_type:
            for err in usr_input.error_rate:
                for injection_rate in usr_input.injection_rate:
                    for err_metric in usr_input.error_metric:
                        anomaly_data_generator(err, t, injection_rate, err_metric,
                                               filename, file_extension, usr_input.data_type, usr_input.variable)


def input_injection_range(arg):
    """ensure the input values to injection_rate are floating numbers between 0 and 1"""

    try:
        f = float(arg)
    except ValueError:
        raise argparse.ArgumentTypeError("Argument must be a floating point number")
    if f < 0 or f > 1:
        raise argparse.ArgumentTypeError("Argument must be between 0 and 1")

    return f


def default_input_file():
    """get the file path of the input files in the data directory"""
    try:
        return [os.path.join(INPUT_DIR, file) for file in os.listdir(INPUT_DIR)]
    except FileNotFoundError:
        # did not find folder INPUT_DIR, this escape is for user specified input file path
        return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='inject anomaly into files.')
    parser.add_argument("-f", "--file", nargs="+", default=default_input_file(),
                        help="user-select the input file instead of using the default input folder")
    parser.add_argument("-o", "--output", type=str, help="customize the location of output files")
    parser.add_argument("-e", "--error_rate", type=float, nargs='+', required=True,
                        help="the value of the error")
    parser.add_argument("-i", "--injection_rate", type=input_injection_range, nargs='+', required=True,
                        help="the frequency of the error, between 0 and 1")
    parser.add_argument("-t", "--anomaly_type", type=int, nargs='+', choices=[0, 1], default=[0],
                        help="select types of error injected, point anomaly by default,"
                             " INCOMPLETE")
    parser.add_argument("-m", "--error_metric", type=str, nargs='+', required=True,
                        choices=['absolute', 'relative', 'point', 'gauss'],
                        help="determine the error injection metric")
    parser.add_argument("-p", "--plot", action="store_true",
                        help="plot the data if true")
    parser.add_argument("--dct", action="store_true",
                        help="run dct comparison if true")
    parser.add_argument("-d", "--data_type", type=str, default='f', choices=['f', 's'],
                        help='indicates if the bin files are in double precision or '
                             'single precision format, double precision by default')
    parser.add_argument("-v", "--variable", type=str,
                        help='used only for nc files, specify which variable to inject errors'
                             'into')
    args = parser.parse_args()
    print(args)

    test_anomaly_gen_hpcdata(args)
