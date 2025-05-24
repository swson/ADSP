############################################################################

# SDC-HPCG: Silent Data Corruption Detection with MTX-based HPCG Benchmark #
############################################################################

This repository contains a modified version of the HPCG benchmark adapted for Silent Data Corruption (SDC) detection research using performance counters. 
This project uses a fixed .mtx sparse matrix file  (e.g., 494_bus.mtx)  as input for the HPCG benchmark.

The system is designed to:

Inject errors into HPCG computations (CG, CG_ref, CG_timed, MG_ref, and SPV_ref)
Collect hardware performance counter data using libpmu tool,
Convert raw output into structured CSV format,
Compare classifier performance for anomaly detection using PMC values.

## Directory Structure

sdc-inference/
├── hpcg-3.1/                 # Modified HPCG benchmark source
│   └── ...                   # HPCG source files (Makefile, *.cpp, *.hpp, etc.)
├── limpmu/                   # PMU monitoring tool
│   └── ...                   # limpmu source code and scripts
├── inference/               
│   ├── raw/                  # Raw PMC output files (txt) after error injection
│   ├── data/                 # Converted CSV files from raw PMC data
│   ├── script_new_494.py     # Converts raw txt files into CSV format
│   ├── 494_bus.mtx           # A fixed .mtx sparse matrix file as input
│   └── inference_analysis.py # Performs anomaly detection and evaluation
├── Makefile                  # Makefile to build hpcg-3.1
└── script_494.sh             # Runs error injection and collects PMC data


## Run SDC-HPCG ##
Build Run make in the root directory. This builds the hpcg-3.1 project under the Linux-Serial configuration.
ex) make

Run Error injection + Data Collection This will:
Inject errors during HPCG computations
Collect PMC data using the limpmu tool
Save raw counter outputs into the inference/raw/ directory

* Before running the script, update the following fields as needed:

|    variable/value       |                               description                                      |
|-------------------------|--------------------------------------------------------------------------------|
| out=~/grid-494          | Output directory to store generated files. Replace with your desired location. |
| HPCG_MATRIX_PATH=/.mtx  | Path to your .mtx file. Update with the full path to your matrix file.         |
| 494 494 1               | the size of your .mtx file                                                     |


ex) ./script_all.sh

Convert Raw to CSV Run script_new.py in the inference/ folder. This converts *.txt files in raw/ folder into .csv files in the data/ folder.
ex) python3 script_new.py

Run Inference Run inference_analysis.py in the inference/ folder. This loads the CSV data, trains anomaly detection classifiers, and outputs evaluation metrics and results with the top 10 PMUs.
ex) python3 inference_analysis.py

* Before running the script, update the following fields as needed:

|   variable/value        |                            description                                    |
|-------------------------|---------------------------------------------------------------------------|
| grid_size=494           | Set this value to match the grid size used in your experiment. If your script_new.sh script processes data from the folder grid-494, then this should be grid_size=494.    |
                              
                                                                           


