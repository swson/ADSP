#! /usr/bin/python

import argparse
import numpy as np
from sys import stdin


# by default, 2.5 sigmas away from mean will be classified as outliers
parser = argparse.ArgumentParser(prog='PROG')
parser.add_argument('--stddev', '-s', action='store', type=float, default=2.5)
args = parser.parse_args()

nstddev = args.stddev

data_in = []

for line in stdin:
	data_in.append(float(line))


# make into numpy array
arr = np.sort(np.array(data_in))

# get standard deviation
std_dev = np.std(arr)

# get mean
mean = np.mean(arr)

# outlier selection
outlier_min = mean - nstddev * std_dev
outlier_max = mean + nstddev * std_dev

outlier_arr = arr[(arr <= outlier_min) | (arr >= outlier_max)]
group_array = arr[(arr > outlier_min) & (arr < outlier_max)]

q = []

for p in [0, 25, 50, 75, 100]:
	q.append(np.percentile(group_array, p))

print(f"""\t\\addplot+[boxplot prepared={{
		\t\tlower whisker={q[0]},
		\t\tlower quartile={q[1]},
		\t\tmedian={q[2]},
		\t\tupper quartile={q[3]},
		\t\tupper whisker={q[4]},
		\t}},]""")

if outlier_arr.size > 0:
	print("\t\ttable[row sep=\\\\, y index=0] {")
	print("\t\t\t" + "\\\\ ".join([str(n) for n in outlier_arr]))
	print("\t\t\\\\ };")
else:
	print("\t\tcoordinates {};")

