import os
import subprocess
import math
from pathlib import Path

# ======================
# CONFIGURATION
# ======================
max_counter = 4
batch_id2 = 0

matrix = "input/494_bus_input/494_bus.mtx.crs"
input_dir = "input/494_bus_input"
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# --------------------------------------------------------
# 1. List of hardware events to monitor (edit as needed)
# --------------------------------------------------------
event_name_arr = [
    'uops_retired.macro_fused',
    'inst_retired.any',
    'branch-loads',
    'br_inst_retired.not_taken',
    'br_inst_retired.conditional',
    'br_inst_retired.cond_ntaken',
    'br_inst_retired.cond',
    'br_inst_retired.all_branches_pebs',
    'br_inst_retired.all_branches',
    'L1-dcache-loads',
    'instructions',
    'inst_retired.any_p',
    'branch-instructions',
    'topdown-slots-retired',
    'mem-stores',
    'mem_inst_retired.all_loads',
    'L1-dcache-stores',
    'br_inst_retired.near_taken',
    'uops_retired.retire_slots',
    'uops_executed.x87',
    'mem_inst_retired.any',
    'mem_inst_retired.all_stores',
    'dTLB-stores',
    'dTLB-loads',
    'arith.divider_active',

    'uops_executed.core',
    'uops_issued.any',
    'idq_uops_not_delivered.core'
  
    # Add more events if needed
]

# --------------------------------------------------------
# 2. CLEAN RUN (baseline without errors)
# --------------------------------------------------------
def perform_run(batch_id, num_runs, max_counter, event_name_arr):
    num_loops_needed = math.ceil(len(event_name_arr) / max_counter)
    base_name = f"{output_dir}/494_bus_point_gauss_0.00_0.{batch_id + 1}.mtx_1"
    os.makedirs(output_dir, exist_ok=True)

    output_file = f"{base_name}.json"
    Path(output_file).touch()

    for run_number in range(num_runs):
        # Create placeholder output file for this run
        Path(f"run_batch{batch_id}_run_{run_number}_outputs.json").touch()

        start = 0
        end = 0
        for total_groups_created in range(1, num_loops_needed + 1):
            print(f"[Batch {batch_id}] (CLEAN) Run {run_number}, Group {total_groups_created}")

            # Determine event group boundaries
            if (total_groups_created * max_counter) > len(event_name_arr):
                end = start + (len(event_name_arr) - start)
            else:
                end = total_groups_created * max_counter

            # Join events into a comma-separated string for perf command
            event_name_string = ",".join(event_name_arr[start:end])

            json_output = f"{base_name}_{total_groups_created}.json"
            perf_cmd = (
                f"sudo perf stat -j -o {json_output} -e {event_name_string} "
                f"./crs_matmult --matrix {matrix} >> /dev/null"
            )

            subprocess.run([perf_cmd], shell=True, check=False)
            if os.path.exists(json_output):
                # Append group output into a single combined JSON
                subprocess.run([f"cat {json_output} >> {output_file}"], shell=True, check=False)
            start = end


# --------------------------------------------------------
# 3. ERROR RUN (runs with injected errors)
# --------------------------------------------------------
def perform_run_error(matrix_file, batch_id, num_runs, max_counter, event_name_arr):
    num_loops_needed = math.ceil(len(event_name_arr) / max_counter)
    matrix_basename = os.path.basename(matrix_file)
    base_name = os.path.join(output_dir, f"{matrix_basename}_{batch_id + 1}")

    output_file = f"{base_name}.json"
    Path(output_file).touch()

    for run_number in range(num_runs):
        start = 0
        end = 0
        for total_groups_created in range(1, num_loops_needed + 1):
            print(f"[Batch {batch_id}] (ERROR) Run {run_number}, Group {total_groups_created}")

            # Determine event group boundaries
            if (total_groups_created * max_counter) > len(event_name_arr):
                end = start + (len(event_name_arr) - start)
            else:
                end = total_groups_created * max_counter

            # Join events for this group
            event_name_string = ",".join(event_name_arr[start:end])
            json_output = f"{base_name}_{total_groups_created}.json"

            perf_cmd = (
                f"sudo perf stat -j -o {json_output} -e {event_name_string} "
                f"./crs_matmult --matrix {matrix_file} >> /dev/null"
            )

            subprocess.run([perf_cmd], shell=True, check=False)
            if os.path.exists(json_output):
                # Append results to the combined output file
                subprocess.run([f"cat {json_output} >> {output_file}"], shell=True, check=False)
            start = end


# --------------------------------------------------------
# 4. MAIN EXECUTION
# --------------------------------------------------------
input_files = sorted([
    os.path.join(input_dir, f)
    for f in os.listdir(input_dir)
    if f.startswith("494_bus_point_gauss_") and f.endswith(".crs")
])

# Run CLEAN (baseline) experiments
for batch_id2 in range(100):
    perform_run(batch_id2, 1, max_counter, event_name_arr)

# Run ERROR (corrupted) experiments
for matrix_file in input_files:
    for batch_id in range(1):
        perform_run_error(matrix_file, batch_id, 1, max_counter, event_name_arr)
