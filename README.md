#  Unified Framework for Error Injection, Benchmarking, and Inference

This repository provides an integrated framework for **error injection**, **HPC benchmarking (HPCG, SpMV)**,  
and **machine learning–based inference and analysis**.  

The framework is designed to support end-to-end research on **Silent Data Corruption (SDC)** and computation error detection —  
covering data preparation, error modeling, benchmark execution, and inference evaluation.

---

##  Repository Structure
<pre lang="md">
root/
│
├── error_injection/    # Error injection modules
│ ├── mtx/              # Inject errors into Matrix Market (.mtx) files
│ └── csv_bin_dat_nc/   # Inject errors into other formats (CSV/BIN/DAT/NC)
│
├── data/
│ ├── dataset/          # Core datasets (e.g., SuiteSparse matrices)
│ └── convert/          # Data conversion and preprocessing tools
│   └── mtx_to_crs.py   # Convert .mtx to CRS format
│
├── benchmarks/         # Benchmark execution and modified HPC codes
│ ├── SpMV_uml/         # Run SpMV (Sparse Matrix-Vector)
│ │ └── spmv_perf/      # Get Performance Monitoring counters values
│ └── HPCG_uml/         # Run Modified HPCG benchmark
│   ├── error_injection/    # Error injection module within HPCG
│   ├── HPCG/               # HPCG source and run scripts
│   └── libpmu/             # PMU-based performance monitoring module
│
├── inference/              # Machine learning–based inference and analysis
│ ├── inference_python/     # Python scripts for LR, DT, RF, MLP models and metrics
│ │ └── preprocess/         # Unify text files into a single CSV file
│ └── inference_jupyter/    # Jupyter notebooks for LR, DT, RF, MLP models and metrics
│
└── README.md           # Project overview and usage guide
</pre>
## Typical Workflow

(1) Prepare datasets     e.g) data/dataset/*.mtx

(2) Inject errors        e.g) error_injection/ → generate corrupted data

(3) Run benchmarks       e.g) benchmarks/HPCG_uml/ → collect PMU performance counters

(4) Perform inference    e.g) inference/inference_python/ or inference/inference_jupyter/

## Citation
If you use this framework in your research, please cite:

M. Choi, T. Azzaoui, K. Chaisson, O. Arias, and S. W. Son. Detecting silent data corruption from hardware counters.
In 2025 IEEE International Conference on Cluster Computing (CLUSTER), 2025.

