import argparse
import math
import os
import random
import sys

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import rcParams
from scipy import fft

import handle_files

INPUT_DIR = "data"
OUTPUT_DIR = "result"
ANOMALY_TYPE_LIST = ["point", "collective"]
READ_FILE = {".bin": handle_files.read_binary_file,
             ".dat": handle_files.read_binary_file,
             ".csv": handle_files.read_csv_file}
WRITE_FILE = {".bin": handle_files.write_binary_file,
              ".dat": handle_files.write_binary_file,
              ".csv": handle_files.write_csv_file}
plot_flag = False
dct_flag = False
PLOT_WINDOW_SIZE = 100
# specific the energy percentage needed to represent
# the DCT coefficients
ENERGY_PERCENTAGE_LIST = [0.95, 0.99]


def anomaly_data_generator(original, error_rate, anomaly_type_num, anomaly_rate, local,
                           filename, file_extension, data_type):
    """inject errors into the original data file and then output the
    anomaly file along with information on error injection"""

    anomaly_type = ANOMALY_TYPE_LIST[anomaly_type_num]
    output_file = output_file_name(OUTPUT_DIR, filename, anomaly_type, error_rate, anomaly_rate, file_extension)
    data_size = len(original)
    error_msg = "local" if local else "global"
    block_size = local if local else data_size
    df_org = pd.Series(original)
    df = df_org.copy()
    # iterate_amount is the number of blocks the data is separated
    # into when --local is selected, this value is rounded up
    iterate_amount = -(df.size // -block_size)
    # mean square error to be reported at the end
    mse = 0.0
    error_num = int(data_size * anomaly_rate)
    # get a list of random errors
    error_list = get_error_list(anomaly_type, data_size, error_num)
    error_list.sort()
    max_error = [None] * iterate_amount

    print("--------------------------------------------")
    print("input filename:  " + filename + file_extension)
    print("output filename:  " + output_file)
    print("error type: ", anomaly_type)
    print("error range: ", error_msg)
    print("data size: ", data_size)
    print("Number of blocks: ", iterate_amount)
    print("Number of errors: ", error_num)
    print("Error list: ", error_list)

    if error_num == 0:
        print("WARNING: Anomaly rate is too low, no errors is injected, an anomaly file will not be created")
        sys.stderr.write("WARNING: Anomaly rate is too low, no errors is injected, "
                         "an anomaly file will not be created\n")
        print("--------------------------------------------")

        return

    # for collective anomaly, data will be separated into blocks and mean values
    # need to be calculated for each blocks to calculate the error range
    for block_index in range(iterate_amount):
        block_start = block_index * block_size
        block_end = (block_index + 1) * block_size
        sub_df = df[block_start:block_end]
        max_error[block_index] = sub_df.mean(0) * error_rate
        print("Block number: ", block_index, " start: ", block_start, " end: ",
              block_end, " error range: ", max_error[block_index])

    # WARNING collective injection not implemented
    for error_index in error_list:
        block_index = error_index // block_size
        # get new error magnitude every time for point injection
        error_value = random.uniform(-max_error[block_index], max_error[block_index])
        df[error_index] = df[error_index] + error_value
        print("Error number ", error_index, " injected at block ", block_index,
              "error range", max_error[block_index], ", error value ", error_value,
              ", originally ", df_org[error_index], ", now ", df[error_index])

        mse += (df_org[error_index] - df[error_index]) ** 2

    mse /= df.size
    print("mean square error: ", mse)

    if dct_flag:
        for energy_percentage in ENERGY_PERCENTAGE_LIST:
            print("Original data needs",
                  get_dct(df_org.tolist(), energy_percentage),
                  "coefficient to represent",
                  energy_percentage, "% for a data size of",
                  df_org.size)
            print("Error injected data needs",
                  get_dct(df.tolist(), energy_percentage),
                  "coefficient to represent",
                  energy_percentage, "% for a data size of",
                  df.size)

    WRITE_FILE[file_extension](df, output_file, data_type)
    print("--------------------------------------------")

    if plot_flag:
        plot_data(df_org, df, error_list, anomaly_type, filename)

    return


def plot_dct(list_new, list_org):
    """plot the dct plot of the old and new data sets, UNUSED
    input: list"""

    dct_new_plot = fft.dct(list_new)
    dct_org_plot = fft.dct(list_org)
    plt.plot(dct_new_plot, c='r')
    plt.plot(dct_org_plot, c='b')
    plt.title("DCT comparison")
    plt.xlabel("Index")
    plt.ylabel("Value")

    plt.show()


def get_dct(list_data, energy_percentage):
    """Run DCT on the data and output the number of coefficients
    needed for that energy percentage"""
    # sum of (dct data points)^2

    list_dct = fft.dct(list_data, norm='ortho')
    num = 0
    dem = 0
    cof_cnt = 0

    for value in list_dct:
        dem += value ** 2

    for value in sorted(list_dct, reverse=True):
        num += value ** 2
        cof_cnt += 1
        # print("num:", num, "dem:", dem, "n/d", num / dem, "value:", value)
        # if (num / dem) ** 0.5 >= energy_percentage:
        if (num / dem) >= energy_percentage:

            return cof_cnt


def get_mse(list_org, list_new):
    """Take in two lists of same length and then
    find the mse between them, UNUSED"""

    if len(list_org) != len(list_new):
        sys.stderr.write("ERROR: original list and error injected list data size mismatch\n")
        exit()

    mse_loc = 0
    for index in range(len(list_org)):
        mse_loc += (list_org[index] - list_new[index]) ** 2

    mse_loc /= len(list_org)

    return mse_loc


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


def output_file_name(folder_name, file_path, anomaly_type, error_rate, anomaly_rate, file_type):
    """create the output file name"""

    (path, file_name) = os.path.split(file_path)

    error_str = str(error_rate).replace(".", "p")
    anomaly_str = str(anomaly_rate).replace(".", "p")

    return os.path.join(folder_name, file_name + "_" + anomaly_type + "_" + error_str + "_" + anomaly_str + file_type)


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

    return error_list


def test_anomaly_gen_hpcdata(file_list, anomaly_type, error_rate, anormal, local=False,
                             plot=False, dct=False, data_type='d'):
    global plot_flag
    global dct_flag
    plot_flag = plot
    dct_flag = dct

    sys.stdout = open('log.txt', 'w')
    # NEED TO DO: put time and run directory into log file
    for f in file_list:
        filename, file_extension = os.path.splitext(f)
        try:
            original = READ_FILE[file_extension](f, data_type)
        except KeyError:
            print(file_extension + " file type not supported")
            continue

        # xscale = get_scale(original)
        # Xa = [ele / xscale for ele in original]
        # original = Xa  # adjust the scale of the original data

        for t in anomaly_type:

            for err in error_rate:
                for anomaly_rate in anormal:
                    anomaly_data_generator(original, err, t, anomaly_rate, local, filename,
                                           file_extension, data_type)


def get_scale(X):
    absX = [abs(ele) for ele in X]
    bs_max = max(absX)
    bs_min = min(absX)
    SF = math.ceil(math.log10(bs_max))
    xscale = pow(10, SF - 1)

    return xscale


def input_anomaly_range(arg):
    """ensure the input values to anomaly_rate are floating numbers between 0 and 1"""

    try:
        f = float(arg)
    except ValueError:
        raise argparse.ArgumentTypeError("Argument must be a floating point number")
    if f < 0 or f > 1:
        raise argparse.ArgumentTypeError("Argument must be between 0 and 1")

    return f


def input_block_size_range(arg):
    """ensure the input values to block size is larger than 0 and is an integer"""

    try:
        i = int(arg)
    except ValueError:
        raise argparse.ArgumentTypeError("Argument must be an integer number")

    if i < 0:
        raise argparse.ArgumentTypeError("Argument must be positive")
    if i == 0:
        raise argparse.ArgumentTypeError("Argument must be non-zero")

    return i


def default_input_file():
    """get the file path of the input files in the data directory"""
    return [os.path.join(INPUT_DIR, file) for file in os.listdir(INPUT_DIR)]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='inject anomaly into files.')
    parser.add_argument("-f", "--file", nargs="+", default=default_input_file(), help="select the file")
    parser.add_argument("-e", "--error_rate", type=float, nargs='+', default=[0.1],
                        help="the value of the error")
    parser.add_argument("-a", "--anomaly_rate", type=input_anomaly_range, nargs='+', default=[0.001],
                        help="the frequency of the error, between 0 and 1")
    parser.add_argument("-l", "--local", type=input_block_size_range,
                        help="if this argument is false, error values will be calculated "
                             "relative to the mean of the entire data set, else it will "
                             "separate the data set into blocks and calculate error "
                             "relative to the mean of the block the error on")
    parser.add_argument("-t", "--anomaly_type", type=int, nargs='+', choices=[0, 1], default=[0],
                        help="select types of error injected, point anomaly by default,"
                             " INCOMPLETE")
    parser.add_argument("-p", "--plot", action="store_true",
                        help="plot the data if true")
    parser.add_argument("--dct", action="store_true",
                        help="run dct comparison if true")
    parser.add_argument("-d", "--data_type", type=str, default='f', choices=['f', 's'],
                        help='indicates if the bin files are in double precision or'
                             'single precision format, double precision by default')
    args = parser.parse_args()
    print(args)

    test_anomaly_gen_hpcdata(args.file, args.anomaly_type, args.error_rate, args.anomaly_rate,
                             args.local, args.plot, args.dct, args.data_type)
