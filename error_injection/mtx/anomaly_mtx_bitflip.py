# Anomaly_mtx.py

import numpy as np
import random
import argparse
import os
import struct

# -------- Noise Functions (Gaussian) --------
def absolute_gauss(value, error_rate):
    noise = np.random.normal(0, abs(value) * error_rate)
    return value + noise

def point_gauss(value, error_rate):
    noise = np.random.normal(value, abs(value) * error_rate)
    return value + noise

# -------- Bit Flip Helper Functions --------
def float_to_bits(value):
    """Convert Python float (IEEE-754 double) to 64-bit int."""
    return struct.unpack('>Q', struct.pack('>d', value))[0]

def bits_to_float(bits):
    """Convert 64-bit int to Python float (IEEE-754 double)."""
    return struct.unpack('>d', struct.pack('>Q', bits))[0]

def flip_mantissa_bits(value, num_bits, start_bit=0, end_bit=51):
    """
    Flip num_bits random bits in the mantissa (52 LSBs) of a double.
    mantissa bit index: 0 (LSB) ~ 51 (MSB)
    """
    if num_bits <= 0:
        return value

    # 유효 범위 클램프
    lo = max(0, start_bit)
    hi = min(51, end_bit)
    if lo > hi:
        # 범위가 말이 안 되면 그냥 원래 값 리턴
        return value

    bits = float_to_bits(value)

    cand_positions = list(range(lo, hi + 1))  # mantissa bit index (0~51)
    num_bits = min(num_bits, len(cand_positions))
    positions = random.sample(cand_positions, num_bits)

    for pos in positions:
        # mantissa는 float의 전체 64비트 중에서 0~51 번째 비트라고 가정 (LSB 기준)
        bits ^= (1 << pos)

    return bits_to_float(bits)

def flip_exponent_bits(value, num_bits, start_bit=0, end_bit=10):
    """
    Flip num_bits random bits in the exponent (11 bits) of a double.
    exponent bit index: 0 (LSB) ~ 10 (MSB)
    실제 64비트 상에서는 위치 52~62에 해당.
    """
    if num_bits <= 0:
        return value

    # 유효 범위 클램프
    lo = max(0, start_bit)
    hi = min(10, end_bit)
    if lo > hi:
        return value

    bits = float_to_bits(value)

    # exponent bit index(0~10)를 실제 비트 위치(52~62)로 매핑
    cand_positions = [52 + i for i in range(lo, hi + 1)]
    num_bits = min(num_bits, len(cand_positions))
    positions = random.sample(cand_positions, num_bits)

    for pos in positions:
        bits ^= (1 << pos)

    return bits_to_float(bits)

# -------- Argument Parsing --------
parser = argparse.ArgumentParser(
    description=(
        "Inject errors into Matrix Market (.mtx) file "
        "using Gaussian noise or bit flips in mantissa/exponent."
    )
)

parser.add_argument('-f', '--file', type=str, required=True,
                    help="Path to input .mtx file")
parser.add_argument('-o', '--output', type=str, required=True,
                    help="Output folder path")
parser.add_argument('-i', '--injection_rate', type=float, required=True,
                    help="Injection rate (e.g., 0.05)")

# 에러 크기 / 비트 플립 모드는 서로 배타적으로 하나만 선택
mode_group = parser.add_mutually_exclusive_group(required=True)
mode_group.add_argument(
    '-e', '--error_rate', type=float,
    help="Gaussian error rate (e.g., 0.1). Used with -m {absolute_gauss, point_gauss}."
)
mode_group.add_argument(
    '-fm', '--flip_mantissa', type=int,
    help="Number of mantissa bits to flip for each value."
)
mode_group.add_argument(
    '-fe', '--flip_exponent', type=int,
    help="Number of exponent bits to flip for each value."
)

parser.add_argument(
    '-m', '--mode', type=str,
    choices=['absolute_gauss', 'point_gauss'],
    default='point_gauss',
    help="Noise mode for Gaussian error: 'absolute_gauss' or 'point_gauss'. "
         "Used only when -e / --error_rate is given."
)

# ---- 선택 비트 범위 옵션 (mantissa / exponent) ----
parser.add_argument(
    '--fm_start', type=int, default=0,
    help="Mantissa bit range start (0-51, 0 = LSB). Used with -fm."
)
parser.add_argument(
    '--fm_end', type=int, default=51,
    help="Mantissa bit range end (0-51, 51 = MSB). Used with -fm."
)

parser.add_argument(
    '--fe_start', type=int, default=0,
    help="Exponent bit range start (0-10, 0 = exponent LSB). Used with -fe."
)
parser.add_argument(
    '--fe_end', type=int, default=10,
    help="Exponent bit range end (0-10, 10 = exponent MSB). Used with -fe."
)

args = parser.parse_args()

input_path = args.file
output_folder = args.output
injection_rate = args.injection_rate
error_rate = args.error_rate
flip_m = args.flip_mantissa
flip_e = args.flip_exponent
fm_start = args.fm_start
fm_end = args.fm_end
fe_start = args.fe_start
fe_end = args.fe_end

# -------- Select Error Injection Function --------
if error_rate is not None:
    # Gaussian 모드
    if args.mode == 'absolute_gauss':
        def inject_error(value):
            return absolute_gauss(value, error_rate)
    else:  # point_gauss
        def inject_error(value):
            return point_gauss(value, error_rate)

elif flip_m is not None:
    # mantissa 비트 플립 모드
    def inject_error(value):
        return flip_mantissa_bits(value, flip_m, fm_start, fm_end)

elif flip_e is not None:
    # exponent 비트 플립 모드
    def inject_error(value):
        return flip_exponent_bits(value, flip_e, fe_start, fe_end)

else:
    raise ValueError("One of -e / -fm / -fe must be specified.")

# -------- Read Input File --------
with open(input_path, 'r') as file:
    lines = file.readlines()

# '%'로 시작하는 라인은 주석, 나머지는 데이터
matrix_data = [line.split() for line in lines if not line.startswith('%')]
header = matrix_data[0]           # e.g., "nrows ncols nnz"
matrix_values = matrix_data[1:]   # actual entries: i j value

# -------- Inject Errors --------
num_entries_to_modify = int(len(matrix_values) * injection_rate)
entries_to_modify = random.sample(matrix_values, num_entries_to_modify) if num_entries_to_modify > 0 else []

for entry in entries_to_modify:
    # 값이 없으면 기본값 1.0 추가 (i, j만 있는 경우)
    if len(entry) < 3:
        entry.append("1.0")

    original_val = float(entry[2])
    modified_val = inject_error(original_val)
    entry[2] = str(modified_val)

modified_lines = [header] + matrix_values

# -------- Prepare Output File --------
os.makedirs(output_folder, exist_ok=True)
input_filename = os.path.splitext(os.path.basename(input_path))[0]

# 파일 이름에 어떤 모드인지 표시
if error_rate is not None:
    mode_tag = args.mode
    output_filename = f"{input_filename}_{mode_tag}_{error_rate:.2f}_{injection_rate:.2f}.mtx"
elif flip_m is not None:
    mode_tag = f"mantissaFlip{flip_m}_b{fm_start}-{fm_end}"
    output_filename = f"{input_filename}_{mode_tag}_{injection_rate:.2f}.mtx"
else:  # flip_e is not None
    mode_tag = f"exponentFlip{flip_e}_b{fe_start}-{fe_end}"
    output_filename = f"{input_filename}_{mode_tag}_{injection_rate:.2f}.mtx"

output_path = os.path.join(output_folder, output_filename)

with open(output_path, 'w') as file:
    # 주석 라인 먼저 그대로 씀
    file.writelines([line for line in lines if line.startswith('%')])
    # 수정된 헤더 및 데이터 라인 출력
    for line in modified_lines:
        file.write(' '.join(line) + '\n')

print(f"Modified matrix saved as '{output_path}'")
