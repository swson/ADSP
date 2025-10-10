import numpy as np
import random
import argparse
import os

# -------- Noise Functions --------
def absolute_gauss(value, error_rate):
    noise = np.random.normal(0, abs(value) * error_rate)
    return value + noise

def point_gauss(value, error_rate):
    noise = np.random.normal(value, abs(value) * error_rate)
    return value + noise

# -------- Argument Parsing --------
parser = argparse.ArgumentParser(description="Inject Gaussian noise into Matrix Market (.mtx) file.")
parser.add_argument('-f', '--file', type=str, required=True, help="Path to input .mtx file")
parser.add_argument('-o', '--output', type=str, required=True, help="Output folder path")
parser.add_argument('-e', '--error_rate', type=float, required=True, help="Error rate (e.g., 0.1)")
parser.add_argument('-i', '--injection_rate', type=float, required=True, help="Injection rate (e.g., 0.05)")
parser.add_argument('-m', '--mode', type=str, choices=['absolute_gauss', 'point_gauss'], default='point_gauss',
                    help="Noise mode: 'absolute_gauss' or 'point_gauss'")
args = parser.parse_args()

# -------- Select Noise Function --------
if args.mode == 'absolute_gauss':
    add_gaussian_noise = absolute_gauss
else:
    add_gaussian_noise = point_gauss

input_path = args.file
output_folder = args.output
error_rate = args.error_rate
injection_rate = args.injection_rate

# -------- Read Input File --------
with open(input_path, 'r') as file:
    lines = file.readlines()

matrix_data = [line.split() for line in lines if not line.startswith('%')]
header = matrix_data[0]
matrix_values = matrix_data[1:]

# -------- Inject Noise --------
num_entries_to_modify = int(len(matrix_values) * injection_rate)
entries_to_modify = random.sample(matrix_values, num_entries_to_modify)

for entry in entries_to_modify:
    if len(entry) < 3:
        entry.append("1.0")
    
    entry[2] = str(add_gaussian_noise(float(entry[2]), error_rate))

modified_lines = [header] + matrix_values

# -------- Prepare Output File --------
os.makedirs(output_folder, exist_ok=True)
input_filename = os.path.splitext(os.path.basename(input_path))[0]
output_filename = f"{input_filename}_{args.mode}_{error_rate:.2f}_{injection_rate:.2f}.mtx"
output_path = os.path.join(output_folder, output_filename)

with open(output_path, 'w') as file:
    file.writelines([line for line in lines if line.startswith('%')])
    for line in modified_lines:
        file.write(' '.join(line) + '\n')

print(f"Modified matrix saved as '{output_path}'")
