from matplotlib import pyplot as plt
from scipy import fft
import numpy as np


def knee_locator(list_data):
    data_length = len(list_data)
    list_dct = fft.dct(list_data, norm='ortho')

    # turns list into numpy array and get the squared data and sum of all data values
    arr = np.array(list_dct)
    arr2 = np.square(arr)
    dem = np.sum(arr2)

    # no knee point if all data is 0
    if dem == 0:
        return float('nan')

    # sort the data in ascending order and get the CDF
    arr2_sort_norm = (-np.sort(-arr2)) / dem
    x_cdf = np.cumsum(arr2_sort_norm)

    ymin = np.min(x_cdf)
    ymax = np.max(x_cdf)
    xmin = 0
    xmax = data_length

    Xsn = np.empty(data_length)
    Ysn = np.empty(data_length)
    Xd = np.empty(data_length)
    Yd = np.empty(data_length)

    # no knee point if data is a straight line
    if ymax == ymin:
        return float('nan')

    # get the normalized data and 'difference data'
    for index in range(0, data_length):
        Xsn[index] = (index - xmin) / (xmax - xmin)
        Ysn[index] = (x_cdf[index] - ymin) / (ymax - ymin)

        Xd[index] = Xsn[index]
        Yd[index] = Ysn[index] - Xsn[index]

    # iterate through the list
    for index in range(1, data_length):
        if Yd[index] > Yd[index - 1] and Yd[index + 1] < Yd[index]:
            need = index
            return need


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


def get_coefficient(list_data, energy_percentage):
    """Run DCT on the data and output the number of coefficients
    needed for that energy percentage"""

    list_dct = fft.dct(list_data, norm='ortho')

    # turns list into numpy array and then square them and sum them up
    arr = np.array(list_dct)
    arr2 = np.square(arr)
    dem = np.sum(arr2)

    arr2_sort_norm = (-np.sort(-arr2)) / dem

    return (np.sqrt(np.cumsum(arr2_sort_norm)) < energy_percentage).argmin() + 1


def get_percentage(list_data, energy_coefficient):
    """Run DCT on the data and output the energy percentage
    needed for that number of coefficients"""

    list_dct = fft.dct(list_data, norm='ortho')

    # turns list into numpy array and then square them and sum them up
    arr = np.array(list_dct)
    arr2 = np.square(arr)
    dem = np.sum(arr2)

    arr2_sort_norm = (-np.sort(-arr2)) / dem

    return np.sqrt(np.cumsum(arr2_sort_norm))[energy_coefficient]

