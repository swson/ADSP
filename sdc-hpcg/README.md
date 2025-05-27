##################################################################
# SDC-HPCG: Silent Data Corruption Detection with HPCG Benchmark #
##################################################################

This repository contains a modified version of the [HPCG benchmark](https://www.hpcg-benchmark.org/) 
adapted for Silent Data Corruption (SDC) detection research using performance counters.

The system is designed to:
- Inject errors into HPCG computations (CG, CG_ref, CG_timed, MG_ref, and SPV_ref)
- Collect hardware performance counter data using `libpmu` tool,
- Convert raw output into structured CSV format,
- Compare classifier performance for anomaly detection using PMC values.

## Directory Structure ##

<pre lang="md">
sdc-inference/
├── hpcg-3.1/                # Modified HPCG benchmark source
│   └── ...                  # HPCG source files (Makefile, *.cpp, *.hpp, etc.)
├── limpmu/                  # PMU monitoring tool
│   └── ...                  # limpmu source code and scripts
├── inference/              
│   ├── raw/                 # Raw PMC output files (txt) after error injection
│   ├── data/                # Converted CSV files from raw PMC data
│   ├── script_new.py        # Converts raw txt files into CSV format
│   └── inference_analysis.py# Performs anomaly detection and evaluation
├── Makefile                 # Makefile to build hpcg-3.1
└── script_all.sh            # Runs error injection and collects PMC data
</pre>

## Run SDC-HPCG ##

1. Build
Run `make` in the root directory. This builds the hpcg-3.1 project under the Linux-Serial configuration.
(See **Build Tips** section below if the build fails or `xhpcg` is missing.)
ex) make

2. Run Error injection + Data Collection
This will:
- Inject errors during HPCG computations
- Collect PMC data using the limpmu tool
- Save raw counter outputs into the inference/raw/ directory

ex) ./script_all.sh

3. Convert Raw to CSV
Run `script_new.py` in the inference/ folder.
This converts *.txt files in raw/ folder into .csv files in the data/ folder.

ex) python3 script_new.py

4. Run Inference
Run `inference_analysis.py` in the inference/ folder.
This loads the CSV data, trains anomaly detection classifiers, and outputs evaluation metrics and results with the top 10 PMUs.

ex) python3 inference_analysis.py

## Build Tips (for HPCG) ##

Before building the HPCG benchmark, ensure the following steps are taken to avoid common build and runtime issues:

1. **Make the configure script executable**  
   Ensure that `configure` in the `hpcg-3.1/` folder has execution permission.
   ```bash
   chmod +x hpcg-3.1/configure

2. **Use full absolute path for HPCG_MATRIX_PATH**
   Some scripts and binaries require the full path to the .mtx file. Set the environment variable explicitly:
   ```bash
   HPCG_MATRIX_PATH=$(pwd)/inference/494_bus.mtx
3. **Clean and recompile if needed**
  If the build fails or xhpcg is missing, you can manually clean and rebuild:
  ```bash
  make clean
  make
   
