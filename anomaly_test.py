import argparse
import math
import os
import random
import sys
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
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
ENERGY_PERCENTAGE_LIST = [0.90, 0.95, 0.99, 0.999, 0.9999]


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
    df_new = df_org.copy()

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
    # print(f"Error list:\n{*error_list,}")

    if error_num == 0:
        print("WARNING: Injection rate is too low, no errors is injected, an error injected file will not be created")
        print("--------------------------------------------")

        return

    table = PrettyTable(["Error Number", "Location", "Original Value", "New Injected Value"])
    table.align = "r"
    for error_num, error_index in enumerate(error_list):
        # do not inject errors if original data is nan
        if not math.isnan(df_org[error_index]):
            df_new[error_index] = get_error(df_org[error_index], error_rate, err_metric)
            table.add_row([error_num, error_index, df_org[error_index], df_new[error_index]])
        else:
            table.add_row([error_num, error_index, df_org[error_index], "--"])

    # print the error injection table
    # print(table)

    mse = get_mse(df_org.tolist(), df_new.tolist())
    print("mean square error: ", mse)
    psnr = get_psnr(df_org, mse)
    print("peak signal-to-noise ratio: ", psnr)
    r_value = get_pearsonr(df_org, df_new)
    print("pearson correlation: ", r_value)

    if dct_flag:
        # precip|lon=144|lat=72|10368
        # sst|lat=180|lon=360|64800
        # soil|lon=240|lat=121|29040
        BLOCK_SIZE = 10368

        # for comparisons with only positive and negative error injection
        df_pos = df_org.copy()
        df_neg = df_org.copy()
        for error_num, error_index in enumerate(error_list):
            if not math.isnan(df_org[error_index]):
                df_pos[error_index] = random.uniform(df_org[error_index], df_org[error_index] * (1 + error_rate))
                df_neg[error_index] = random.uniform(df_org[error_index] * (1 - error_rate), df_org[error_index])

        block_num = df_org.size // BLOCK_SIZE
        print("Separated into", block_num, "blocks")

        df_org_list = df_org.tolist()
        df_new_list = df_new.tolist()
        df_pos_list = df_pos.tolist()
        df_neg_list = df_neg.tolist()

        org_k_val = []
        new_k_val = []
        pos_k_val = []
        neg_k_val = []

        for index in range(0, block_num):
            list_start = index * BLOCK_SIZE
            list_end = (index + 1) * BLOCK_SIZE

            df_org_seg = list(df_org_list[list_start: list_end])
            df_org_seg = [x for x in df_org_seg if not math.isnan(x)]

            df_new_seg = list(df_new_list[list_start: list_end])
            df_new_seg = [x for x in df_new_seg if not math.isnan(x)]

            df_pos_seg = list(df_pos_list[list_start: list_end])
            df_pos_seg = [x for x in df_pos_seg if not math.isnan(x)]

            df_neg_seg = list(df_neg_list[list_start: list_end])
            df_neg_seg = [x for x in df_neg_seg if not math.isnan(x)]

            kneel_org = dct.knee_locator(df_org_seg)
            kneel_new = dct.knee_locator(df_new_seg)
            kneel_pos = dct.knee_locator(df_pos_seg)
            kneel_neg = dct.knee_locator(df_neg_seg)

            # print("Block", index + 1)
            # print("Original Knee point is", kneel_org)
            # print("New      Knee point is", kneel_new)
            # print("Positive Knee point is", kneel_pos)
            # print("Negative Knee point is", kneel_neg)

            # if kneel_org == kneel_new:
            #     print("Knee MATCH")
            # else:
            #     print("Knee MISMATCH")

            if kneel_org != None:
                org_k_val.append(kneel_org)
            if kneel_new != None:
                new_k_val.append(kneel_new)
            if kneel_pos != None:
                pos_k_val.append(kneel_pos)
            if kneel_neg != None:
                neg_k_val.append(kneel_neg)

        org_k_val = np.asarray(org_k_val)
        org_k_val = org_k_val[~np.isnan(org_k_val)]
        new_k_val = np.asarray(new_k_val)
        new_k_val = new_k_val[~np.isnan(new_k_val)]
        pos_k_val = np.asarray(pos_k_val)
        pos_k_val = pos_k_val[~np.isnan(pos_k_val)]
        neg_k_val = np.asarray(neg_k_val)
        neg_k_val = neg_k_val[~np.isnan(neg_k_val)]

        print_hist(org_k_val, "Original")
        print_hist(new_k_val, "New     ")
        print_hist(pos_k_val, "Positive")
        print_hist(neg_k_val, "Negative")

        fig, axs = plt.subplots(3, sharex=True)
        fig.suptitle(filename + "_i" + str(injection_rate) + "_e" + str(error_rate) + "_box" + str(BLOCK_SIZE))

        axs[0].hist(org_k_val, bins=50, alpha=0.5, label='original')
        axs[0].hist(new_k_val, bins=50, alpha=0.5, color='r', label='error')
        axs[0].set_title('Dual error bound')

        axs[1].hist(org_k_val, bins=50, alpha=0.5, label='original')
        axs[1].hist(pos_k_val, bins=50, alpha=0.5, color='r', label='error')
        axs[1].set_title('Positive error bound')

        axs[2].hist(org_k_val, bins=50, alpha=0.5, label='original')
        axs[2].hist(neg_k_val, bins=50, alpha=0.5, color='r', label='error')
        axs[2].set_title('Negative error bound')

        plt.setp(axs, ylabel='k count')
        plt.grid(visible=True, which='both', axis='both')
        axs[2].set(xlabel='k value')
        plt.legend()
        # plt.savefig(path + "i" + str(injection_rate) + "_e" + str(error_rate) + ".png")

        plt.show()

        # plt.hist(org_k_val[~np.isnan(org_k_val)], bins=50, alpha=0.5, label='original')
        # plt.hist(new_k_val[~np.isnan(new_k_val)], bins=50, alpha=0.5, color='r', label='error')
        # plt.title(filename + "_i" + str(injection_rate) + "_e" + str(error_rate))
        # plt.ylabel("k count")
        # plt.xlabel("k value")
        # plt.legend()
        # # plt.savefig(path + "i" + str(injection_rate) + "_e" + str(error_rate) + ".png")
        # plt.show()

    if file_extension == ".nc":
        WRITE_FILE[file_extension](df_new, filename + file_extension, output_file, variable, dimension)
    else:
        WRITE_FILE[file_extension](df_new, output_file, data_type)
    print("--------------------------------------------")

    if plot_flag:
        plot_data(df_org, df_new, error_list, anomaly_type, filename)

    return


def get_error(cur_val, para, err_metric):
    """return the error injected value
    input:
    cur_val     -   current data value
    para        -   input parameter
    err_metric  -   type of error

    there are three error metric: absolute, relative, and point
    absolute_uni   -    return a random floating point number between
                        cur_val-para and cur_val+para
    relative_uni   -    return a random floating point number between
                        cur_val-(max-min)*para and cur_val+(max-min)*para
    point_uni      -    return a random floating point number between
                        cur_val-cur_val*para, cur_val+cur_val*para
    absolute_gauss -    return a random floating point number based
                        on a Gaussian distribution with a mean of 0
                        and standard deviation of para
    point_gauss    -    return a random floating point number based
                        on a Gaussian distribution with a mean of cur_val
                        and standard deviation of para
    """
    # print(para)
    if err_metric == "absolute_uni":
        return random.uniform(cur_val - para, cur_val + para)
    elif err_metric == "relative_uni":
        return random.uniform(cur_val - para, cur_val + para)
    elif err_metric == "point_uni":
        return random.uniform(cur_val * (1 - para), cur_val * (1 + para))
    elif err_metric == "absolute_gauss":
        return cur_val + random.gauss(0, para)
    elif err_metric == "point_gauss":
        return cur_val + random.gauss(cur_val, para)
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


def get_psnr(df_org, mse):
    """Take in the original series and mse to
    find the psnr"""

    # if mse is 0, the two data are the same
    if mse == 0:
        return float('nan')

    return 10 * math.log10((df_org.max() - df_org.min()) ** 2 / mse)


def get_pearsonr(x, y):
    """Take in the original data and error injected
    series to find the pearson correlation
    Following the formula from
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html
    """

    m_x = np.nanmean(x)
    m_y = np.nanmean(y)
    r = np.sum((x - m_x) * (y - m_y)) / (np.sum((x - m_x) ** 2) * np.sum((y - m_y) ** 2)) ** 0.5

    return r


def print_hist(np_array, name):
    print(name, "mean k is      ", np.mean(np_array))
    # print(name, "max k count is ", np.bincount(np_array).argmax())
    print(name, "k range is     ", np.amin(np_array), "to", np.amax(np_array))


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
                        # choices=['absolute', 'relative', 'point', 'gauss'],
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
