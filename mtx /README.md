# Error Injection for Sparse Matrices

This repository contains tools for injecting errors into sparse matrix files.

## Usage

### 1. Injecting Noise into a Matrix

You can run the `anomaly_mtx.py` script to inject Gaussian error into an `.mtx` file:

  ```bash
  python anomaly_mtx.py -f data/494_bus.mtx -o result/ -e 0.1 -i 0.05 -m point_gauss

*Arguments:
-f or --file: Path to the input .mtx file.
-o or --output: Path to the folder where the modified file will be saved.
-e or --error_rate: Error rate (e.g., 0.1 means 10% of the value is used as stddev for noise).
-i or --injection_rate: Fraction of non-zero values to modify (e.g., 0.05 = 5%).
-m or --mode: Noise mode, either point_gauss or absolute_gauss.

### 2. Running Batch Experiments
To run multiple combinations of error rates and injection rates automatically:

  ```bash
  python anomaly_exp.py

*This will:
- Run experiments with error_rate from 0.1 to 1.0 in steps of 0.1
- Run experiments with injection_rate from 0.01 to 0.1 in steps of 0.01
- Apply point_gauss noise to each configuration
- Save each noisy matrix to the result/ directory with filenames like:

  ```bash
  494_bus_point_gauss_gauss_0.10_0.01.mtx
