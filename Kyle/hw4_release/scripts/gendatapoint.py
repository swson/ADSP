#! /usr/bin/python

import argparse
import numpy as np
from sys import stdin

# by default, we will try to get CPU data dynamically
parser = argparse.ArgumentParser(prog='PROG')
parser.add_argument('--matrix', '-m', action='store', type=str, required=True)
args = parser.parse_args()

matrix_name = args.matrix
values = []

for line in stdin:
	values.append(float(line))

arr = np.sort(np.array(values))

q = []
for p in [0, 50, 100]:
	q.append(np.percentile(arr, p))

print(f"{matrix_name}\t{q[1]}\t{q[1]-q[0]}\t{q[2]-q[1]}")
