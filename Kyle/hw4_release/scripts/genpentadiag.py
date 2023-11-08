#! /usr/bin/python

from scipy import sparse, io
import numpy as np

def pentadiag(a, b, c, d, e, k0 = -2, k1=-1, k2=0, k3=1, k4 = 2):
	return np.diag(b, k1) + np.diag(c, k2) + np.diag(d, k3) + \
			np.diag(a, k0) + np.diag(e, k4)

a = [1] * 998
b = [1] * 999
c = [1] * 1000
d = [1] * 999
e = [1] * 998

m = sparse.csr_matrix(pentadiag(a, b, c, d, e))
io.mmwrite("penta_diagonal.mtx", m)
