###########################################################################################################################

# SDC-HPCG: Silent Data Corruption Detection with MTX-based HPCG Benchmark #
###########################################################################################################################

This repository contains a modified version of the HPCG benchmark adapted for Silent Data Corruption (SDC) detection research using performance counters. 
This project uses a fixed .mtx sparse matrix file  (e.g., 494_bus.mtx)  as input for the HPCG benchmark.

The system is designed to:

Inject errors into HPCG computations (CG, CG_ref, CG_timed, MG_ref, and SPV_ref)
Collect hardware performance counter data using libpmu tool,
Convert raw output into structured CSV format,
Compare classifier performance for anomaly detection using PMC values.

## Directory Structure ##
<pre lang="md">
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
</pre>

## install the required Python packages ##
```bash
python3 -m pip install seaborn pandas matplotlib numpy scipy scikit-learn
```

If `pip` is not installed on your system, install it first:
```bash
sudo apt update
sudo apt install -y python3-pip
```

## Build HPCG

Run the following commands from the repository root directory:
```bash
chmod +x hpcg-3.1/configure
chmod +x hpcg-3.1/build/bin/xhpcg
make
```

If you want to rebuild from scratch:
```bash
cd hpcg-3.1
make clean
make
cd ..
```

## Run SDC-HPCG

### 1. Run Error Injection + Data Collection

This step will:

- Inject errors during HPCG computations
- Collect PMC data using the `limpmu` tool
- Save raw counter outputs into the `inference/raw/` directory

* Before running the script, update the following fields as needed:

|    variable/value       |                               description                                      |
|-------------------------|--------------------------------------------------------------------------------|
| out=~/grid-494          | Output directory to store generated files. Replace with your desired location. |
| HPCG_MATRIX_PATH=/.mtx  | Path to your .mtx file. Update with the full path to your matrix file.         |
| 494 494 1               | the size of your .mtx file                                                     |

Run:
```bash
./script_all.sh
```

Example:
```bash
(base) mchoi@node0:~/ADSP/benchmarks/HPCG_uml/sdc-mtx$ ./script_all.sh
```
### 2. Convert Raw PMC Output to CSV

Run the conversion script in the `inference/` directory.  
This converts `*.txt` files in the `raw/` folder into `.csv` files in the `data/` folder.
```bash
cd inference
python3 script_new_494.py
```

Example:
```bash
(base) mchoi@node0:~/ADSP/benchmarks/HPCG_uml/sdc-mtx/inference$ python3 script_new_494.py
```

### 3. Run Inference
Run the inference script in the `inference/` directory.  
This loads the CSV data, trains anomaly detection classifiers, and outputs evaluation metrics and results with the top PMUs.
```bash
python3 inference_analysis_once.py
```

Example:
```bash
(base) mchoi@node0:~/ADSP/benchmarks/HPCG_uml/sdc-mtx/inference$ python3 inference_analysis_once.py

* Before running the script, update the following fields as needed:

|   variable/value        |                            description                                    |
|-------------------------|---------------------------------------------------------------------------|
| grid_size=494           | Set this value to match the grid size used in your experiment. If your script_new.sh script processes data from the folder grid-494, then this should be grid_size=494.    |

## Full Example Workflow

The following is an example workflow from build to inference:

```bash
(base) mchoi@node0:~/ADSP/benchmarks/HPCG_uml/sdc-mtx$ chmod +x hpcg-3.1/configure
(base) mchoi@node0:~/ADSP/benchmarks/HPCG_uml/sdc-mtx$ chmod +x hpcg-3.1/build/bin/xhpcg
(base) mchoi@node0:~/ADSP/benchmarks/HPCG_uml/sdc-mtx$ make

(base) mchoi@node0:~/ADSP/benchmarks/HPCG_uml/sdc-mtx/hpcg-3.1$ make clean
(base) mchoi@node0:~/ADSP/benchmarks/HPCG_uml/sdc-mtx/hpcg-3.1$ make

(base) mchoi@node0:~/ADSP/benchmarks/HPCG_uml/sdc-mtx/hpcg-3.1$ sudo apt update
(base) mchoi@node0:~/ADSP/benchmarks/HPCG_uml/sdc-mtx/hpcg-3.1$ sudo apt install -y python3-pip
(base) mchoi@node0:~/ADSP/benchmarks/HPCG_uml/sdc-mtx/hpcg-3.1$ python3 -m pip install seaborn pandas matplotlib numpy scipy scikit-learn

# Run Error Injection + Data Collection
(base) mchoi@node0:~/ADSP/benchmarks/HPCG_uml/sdc-mtx$ ./script_all.sh

# Convert Raw to CSV
(base) mchoi@node0:~/ADSP/benchmarks/HPCG_uml/sdc-mtx/inference$ python3 script_new_494.py

# Run Inference
(base) mchoi@node0:~/ADSP/benchmarks/HPCG_uml/sdc-mtx/inference$ python3 inference_analysis_once.py
```

                                                                           


