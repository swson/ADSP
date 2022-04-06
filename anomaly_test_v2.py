import argparse
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
             ".csv": handle_files.read_csv_file,
             ".nc":  handle_files.read_nc_file}
WRITE_FILE = {".bin": handle_files.write_binary_file,
              ".dat": handle_files.write_binary_file,
              ".csv": handle_files.write_csv_file,
              ".nc":  handle_files.write_nc_file}
plot_flag = False
dct_flag = False
PLOT_WINDOW_SIZE = 100
# specific the energy percentage needed to represent
# the DCT coefficients
ENERGY_PERCENTAGE_LIST = [0.95, 0.99]


def anomaly_data_generator(error_rate, anomaly_type_num, anomaly_rate, err_metric,
                           filename, file_extension, data_type, variable):
    """inject errors into the original data file and then output the
    anomaly file along with information on error injection"""

    # nc files are handled differently since they are more complex
    if file_extension == ".nc":
        if variable is None:
            print("WARNING: Variable is not given for nc files, error files will not be created")
            return
        original, dimension = READ_FILE[file_extension](filename + file_extension, variable)
    else:
        original = READ_FILE[file_extension](filename + file_extension, data_type)

    anomaly_type = ANOMALY_TYPE_LIST[anomaly_type_num]
    output_file = output_file_name(OUTPUT_DIR, filename, anomaly_type, error_rate, anomaly_rate, file_extension)
    data_size = len(original)

    df_org = pd.Series(original)
    df = df_org.copy()

    # mean square error to be reported at the end
    mse = 0.0
    error_num = int(data_size * anomaly_rate)
    # get a list of random errors
    error_list = get_error_list(anomaly_type, data_size, error_num)
    error_list.sort()
    cnt = 1

    print("--------------------------------------------")
    print("input filename:  " + filename + file_extension)
    print("output filename:  " + output_file)
    print("error type: ", anomaly_type)
    print("error metrics: ", err_metric)
    print("data size: ", data_size)
    print("Number of errors: ", error_num)
    print("Error list: ", error_list)

    if error_num == 0:
        print("WARNING: Anomaly rate is too low, no errors is injected, an anomaly file will not be created")
        # sys.stderr.write("WARNING: Anomaly rate is too low, no errors is injected, "
        #                  "an anomaly file will not be created\n")
        print("--------------------------------------------")

        return

    if err_metric == "relative":
        print("max", df_org.max(0), "min", df_org.min(0))
        err_para = (df_org.max(0) - df_org.min(0)) * error_rate
    else:
        err_para = error_rate

    for error_index in error_list:
        df[error_index] = get_error(df[error_index], err_para, err_metric)
        print("Error number ", cnt, " injected at ", error_index,
              ", originally ", df_org[error_index], ", now ", df[error_index])
        cnt += 1
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
    else:
        print("ERROR: Invalid error metrics")
        sys.stderr.write("ERROR: Invalid error metrics\n")
        quit()


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
        return

    return error_list


def test_anomaly_gen_hpcdata(usr_input):

    global plot_flag
    global dct_flag
    plot_flag = usr_input.plot
    dct_flag = usr_input.dct

    sys.stdout = open('log.txt', 'w')
    # NEED TO DO: put time and run directory into log file
    for f in usr_input.file:
        filename, file_extension = os.path.splitext(f)
        if not (READ_FILE.get(file_extension)):
            print("WARNING: " + file_extension + " file type not supported")
            continue

        for t in usr_input.anomaly_type:
            for err in usr_input.error_rate:
                for anomaly_rate in usr_input.anomaly_rate:
                    for err_metric in usr_input.error_metric:
                        anomaly_data_generator(err, t, anomaly_rate, err_metric,
                                               filename, file_extension, usr_input.data_type, usr_input.variable)


def input_anomaly_range(arg):
    """ensure the input values to anomaly_rate are floating numbers between 0 and 1"""

    try:
        f = float(arg)
    except ValueError:
        raise argparse.ArgumentTypeError("Argument must be a floating point number")
    if f < 0 or f > 1:
        raise argparse.ArgumentTypeError("Argument must be between 0 and 1")

    return f


def default_input_file():
    """get the file path of the input files in the data directory"""
    return [os.path.join(INPUT_DIR, file) for file in os.listdir(INPUT_DIR)]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='inject anomaly into files.')
    parser.add_argument("-f", "--file", nargs="+", default=default_input_file(), help="select the file")
    parser.add_argument("-e", "--error_rate", type=float, nargs='+', required=True,
                        help="the value of the error")
    parser.add_argument("-a", "--anomaly_rate", type=input_anomaly_range, nargs='+', required=True,
                        help="the frequency of the error, between 0 and 1")
    parser.add_argument("-t", "--anomaly_type", type=int, nargs='+', choices=[0, 1], default=[0],
                        help="select types of error injected, point anomaly by default,"
                             " INCOMPLETE")
    parser.add_argument("-m", "--error_metric", type=str, nargs='+', required=True,
                        choices=['absolute', 'relative', 'point'],
                        help="determine the error injection metric")
    parser.add_argument("-p", "--plot", action="store_true",
                        help="plot the data if true")
    parser.add_argument("--dct", action="store_true",
                        help="run dct comparison if true")
    parser.add_argument("-d", "--data_type", type=str, default='f', choices=['f', 's'],
                        help='indicates if the bin files are in double precision or'
                             'single precision format, double precision by default')
    parser.add_argument("-v", "--variable", type=str,
                        help='used only for nc files, specify which variable to inject errors'
                             'into')
    args = parser.parse_args()
    print(args)

    test_anomaly_gen_hpcdata(args)
