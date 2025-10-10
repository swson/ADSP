## CSR SpMV experiments using Linux perf

It (1) collects a filtered set of PMU events, (2) runs a clean baseline on a fixed CRS matrix, and (3) runs error-injected variants, measuring with a limited number of hardware counters (max_counter = 4) per run
e.g) `ADSP/benchmarks/SpMV_uml/matmult-progs/crs_matmult/run_combined_exec.py`


## How to run
# Path
`cd ADSP/benchmarks/SpMV_uml/matmult-progs/crs_matmult`
# CRS matrices prepared in input/494_bus_input/ using `error_injection/anomaly_exp.py` and `data/convert/multiple_mtx2crs.py'.
- Baseline path defaults to: input/494_bus_input/494_bus.mtx.crs
- Error-injected files are discovered by glob: 494_bus_point_gauss_*.crs
# Run the experiment
'python3 run_combined_exec.py'

# What happens:
- Generates filtered_events.json via perf list -j.
- Runs 100 clean batches by default (for batch_id2 in range(100): ...).
- Iterates all matched error-injected .crs files (100 cases)



