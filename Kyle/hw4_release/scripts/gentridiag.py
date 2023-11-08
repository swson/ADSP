#! /usr/bin/python

from scipy import sparse, io
import numpy as np

def tridiag(a, b, c, k1=-1, k2=0, k3=1):
	return np.diag(a, k1) + np.diag(b, k2) + np.diag(c, k3)

a = [1] * 10179
b = [1] * 10180
c = [1] * 10179

m = sparse.csr_matrix(tridiag(a, b, c))
io.mmwrite("largetridiagonal.mtx", m)
