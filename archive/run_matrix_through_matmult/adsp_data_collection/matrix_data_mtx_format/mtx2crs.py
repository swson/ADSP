#! /usr/bin/python3

from sys import stdin
from operator import itemgetter

def check_header(hdr):
	hdr = hdr.split()
	return (len(hdr) == 5) and (hdr[0][0:2] == "%%") and \
			(hdr[0][2:] == "MatrixMarket") and \
			(hdr[1] == "matrix") and \
			(hdr[2] == "coordinate") and \
			(hdr[3] in ["pattern", "real", "integer"]) and \
			(hdr[4] in ["general", "symmetric"])
			

def get_matrix_type(hdr):
	return hdr.split()[4]

matrix_data = []
matrix_dict = {}
matrix_type = ""

for count, line in enumerate(stdin):
	# remove leading and trailing whitespaces
	line = line.strip()

	# check header
	if count == 0:
		if not check_header(line):
			raise Exception('Invalid header')
		matrix_type = get_matrix_type(line)
	
	# if we have a comment, ignore it
	if line[0] == '%':
		continue

	# tokenize
	data = line.split()

	if len(matrix_data) == 0 and len(data) == 3:
		# if we do not have matrix data setup, set it up
		matrix_data = data
		continue
	
	# we have matrix data
	key = int(data[0])
	arg = (int(data[1]), 1.0 if len(data) == 2 else float(data[2]))
	
	if key in matrix_dict:
		# we already have this row on the dictionary, just add it
		matrix_dict[key].append(arg)
	else:
		# need to add a row to the dictionary
		matrix_dict[key] = [arg]

# print(f"{matrix_type[0]}\n{matrix_data[2]}\n{matrix_data[0]}")
print(f"{matrix_type[0]}")		# matrix type (g or s)
print(f"{matrix_data[2]}")		# number of values

mat = sorted(matrix_dict.items(), key=itemgetter(0))

a = []
ia = [1]
ja = []
last_row = 0;

# for row, cols in mat:
# 	if row - last_row > 1:
# 		ia.append([0] * (row - last_row))
# 	else:
# 		last_size = ia[-1]
# 		ia.append(last_size + len(cols))
# 		for col, value in cols:
# 			ja.append(col)
# 			a.append(value)
# 	last_row = row

for row, col_value_pair in mat:
	if row - last_row > 1:
		ia.extend([ia[-1]] * (row - last_row - 1))
	ia.append(ia[-1] + len(col_value_pair))
	for col, value in col_value_pair:
		ja.append(col)
		a.append(value)
	last_row = row

print(len(ia))					# number of items in row list

for val in a + ja + ia:
	print(val)
