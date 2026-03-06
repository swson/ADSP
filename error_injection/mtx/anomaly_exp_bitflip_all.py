import subprocess
import numpy as np

matrix_names = ["494_bus", "662_bus", "1138_bus", "bcsstk01", "bcsstk19", "bcsstk20", "bfwb62", "bfwb398", "bfwb782"]
dataset_range = range(1, 6)  # 1~5

for matrix_name in matrix_names:
    for dataset_id in dataset_range:

        # Setting
        input_file = f"./data/{matrix_name}.mtx"
        output_dir = f"./result_bitflip_LSB/{matrix_name}_{dataset_id}/mtx/non_zero"

        # Flip bit positions: 0, 2, 4, 6, 8  (step 2)
        #flip_bits = range(43, 52, 2)
        flip_bits = range(0, 9, 2)

        # Injection rate: 0.01 ~ 0.10 (step 0.005)
        injection_rates = np.arange(0.01, 0.1001, 0.005)

        for bit in flip_bits:
            for inj in injection_rates:
                command = [
                    'python', 'anomaly_mtx_bitflip.py',
                    '-f', input_file,
                    '-o', output_dir,
                    '-i', f'{inj:.3f}',     # 0.005 step이라 3자리로 권장
                    '-fm', '1',             # mantissa 1-bit flip
                    '--fm_start', str(bit), # 정확히 이 bit만
                    '--fm_end', str(bit)
                ]
                print(f"Running: {' '.join(command)}")
                subprocess.run(command, check=True)
