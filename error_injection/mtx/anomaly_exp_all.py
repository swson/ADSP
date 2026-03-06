import subprocess
import numpy as np

# Setting 
input_file = 'data/bfwb782.mtx'
output_dir = 'result_point_original_avg/bfwb782_5/mtx/non_zero'
mode = 'point_gauss'


# Error rate: 0.1 ~ 1.0 (step 0.1)
error_rates = np.arange(0.1, 1.01, 0.1)

# Injection rate: 0.01 ~ 0.1 (step 0.01)
injection_rates = np.arange(0.01, 0.101, 0.01)

for e in error_rates:
    for i in injection_rates:
        command = [
            'python', 'anomaly_mtx.py',
            '-f', input_file,
            '-o', output_dir,
            '-e', f'{e:.2f}',
            '-i', f'{i:.2f}',
            '-m', mode
        ]
        print(f"Running: {' '.join(command)}")
        subprocess.run(command)
