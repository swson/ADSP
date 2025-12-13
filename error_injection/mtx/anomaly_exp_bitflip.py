import subprocess
import numpy as np

# Setting
input_file = 'data/bcsstk01.mtx'
output_dir = 'result_bcsstk01_bitflip_MSB/'

# Flip bit positions: 0, 2, 4, 6, 8  (step 2)
flip_bits = range(43, 52, 2)

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
