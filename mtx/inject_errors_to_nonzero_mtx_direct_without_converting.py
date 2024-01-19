import numpy as np
import math
import random

# Function for absolute Gaussian noise
def absolute_gauss(value, error_rate):
    noise = np.random.normal(0, abs(value) * error_rate)
             
    return value + noise

# Function for point Gaussian noise
def point_gauss(value, error_rate):
    noise = np.random.normal(value, abs(value) * error_rate)
    
    return value + noise

# Choose which noise function to use
add_gaussian_noise = point_gauss  # Change to absolute_gauss if needed

# Parameters
error_rate = 0.10  # error rate
injection_rate = 0.10  # injection rate

# Read the file
with open('C:\\Work\\School\\Coding\\ADSP\\bcsstm38\\bcsstm38.mtx', 'r') as file:
    lines = file.readlines()

# Identify the data lines (excluding comments and the first line)
matrix_data = [line.split() for line in lines if not line.startswith('%')]
header = matrix_data[0]

# Skip the first line (dimensions)
matrix_values = matrix_data[1:]

# Determine the number of entries to modify (elements to inject noise)
num_entries_to_modify = int(len(matrix_values) * injection_rate)

# Randomly select entries to modify
entries_to_modify = random.sample(matrix_values, num_entries_to_modify)

# Add Gaussian noise to the selected entries
for entry in entries_to_modify:
    entry[2] = str(add_gaussian_noise(float(entry[2]), error_rate))

# Combine the comments, header, and modified data
modified_lines = [header] + matrix_values


# Write the modified matrix back to a file
with open('C:\\Work\\School\\Coding\\ADSP\\result_0118_2024\\bcsstm38_gauss_0p10_0p10_nonzero.mtx', 'w') as file:
    # Write the comments
    file.writelines([line for line in lines if line.startswith('%')])
    
    for line in modified_lines:
        file.write(' '.join(line) + '\n')

print("Modified matrix saved as 'sparse_pnp_modified.mtx'")
