# CSR SpMV experiments using Linux perf

It (1) collects a filtered set of PMU events, (2) runs a clean baseline on a fixed CRS matrix, and (3) runs error-injected variants, measuring with a limited number of hardware counters (max_counter = 4) per run
e.g) `ADSP/benchmarks/SpMV_uml/matmult-progs/crs_matmult/run_combined_exec.py`


## How to run
### Path
`cd ADSP/benchmarks/SpMV_uml/matmult-progs/crs_matmult`
### CRS matrices prepared in input/494_bus_input/ using `error_injection/anomaly_exp.py` and `data/convert/multiple_mtx2crs.py`.
- Baseline path defaults to: input/494_bus_input/494_bus.mtx.crs
- Error-injected files are automatically detected based on their filenames, following the pattern 494_bus_point_gauss_*.crs.
### Run the experiment
`python3 run_combined_exec.py`

### What happens:
- Generates filtered_events.json via `perf list -j`.
- Runs HPCG or SpMV on the clean (error-free) matrix for 100 iterations.
- Runs HPCG or SpMV on all error-injected .crs files (100 cases).
- Collects Performance Monitoring Counters (PMCs) for each run.


