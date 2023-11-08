#! /usr/bin/python

import argparse
import numpy as np
from sys import stdin
from scipy import sparse as sm
from scipy import io
from os import path


parser = argparse.ArgumentParser(prog='PROG')
parser.add_argument('--matrix', '-m', action='store', type=str, required=True)
args = parser.parse_args()


my_path = path.dirname(path.abspath(__file__))

matrix_name = args.matrix
values = []

m = sm.csr_matrix(io.mmread(my_path +
		f"/../mat/{matrix_name}/{matrix_name}.mtx"))
nnz = m.getnnz()
nnzd = np.count_nonzero(m.diagonal())

for line in stdin:
	values.append(float(line))

arr = np.sort(np.array(values))

q = []
for p in [0, 50, 100]:
	q.append(np.percentile(arr, p))


# ( 4 x nnzf) – (2 x nnzd)/ Tcrs
flops = []
for t in q:
	flops.append((4 * nnz - 2 * nnzd)/t)

print(f"{matrix_name}\t{flops[1]}\t{flops[1]-flops[2]}\t{flops[0]-flops[1]}")
