import os
import subprocess
import math
from pathlib import Path

# ======================
# CONFIGURATION
# ======================
max_counter = 4
batch_id2 = 0

matrix = "input/sample_input/sample_3.mtx.crs"
input_dir = "input/sample_input"
output_dir = "output_sample_bit51/out_sample_bit51_simple_10time"
os.makedirs(output_dir, exist_ok=True)

# --------------------------------------------------------
# 1. List of hardware events to monitor (edit as needed)
# --------------------------------------------------------
event_name_arr = [

    # ===== Standard HW =====
    'cycles',
    'instructions',
    'branches',
    'branch-misses',
    'cache-references',
    'ref-cycles',
    'bus-cycles',

    # ===== Core PMU – Divider / FP =====
    'arith.divider_active',
    'uops_executed.x87',
    'fp_arith_inst_retired.scalar',
    'fp_arith_inst_retired.scalar_double',
    'fp_arith_inst_retired.vector',
    'fp_arith_inst_retired.128b_packed_double',
    'fp_arith_inst_retired.256b_packed_double',

    # ===== Retired / Uops =====
    'uops_retired.macro_fused',
    'uops_retired.retire_slots',
    'uops_retired.total_cycles',
    'uops_retired.stall_cycles',
    'uops_executed.core',
    'uops_executed.thread',
    'uops_executed.stall_cycles',
    'uops_executed.core_cycles_none',
    'uops_executed.core_cycles_ge_1',
    'uops_executed.core_cycles_ge_2',
    'uops_executed.core_cycles_ge_3',
    'uops_executed.core_cycles_ge_4',

    # ===== Resource / Backend =====
    'resource_stalls.any',
    'resource_stalls.sb',
    'cycle_activity.stalls_total',
    'cycle_activity.stalls_mem_any',
    'cycle_activity.stalls_l1d_miss',
    'cycle_activity.stalls_l2_miss',
    'cycle_activity.cycles_l1d_miss',
    'cycle_activity.cycles_l2_miss',
    'partial_rat_stalls.scoreboard',

    # ===== Memory / Cache =====
    'l1d_pend_miss.pending',
    'l1d_pend_miss.pending_cycles',
    'l1d_pend_miss.pending_cycles_any',
    'l1d_pend_miss.fb_full',
    'l2_rqsts.references',
    'l2_rqsts.miss',
    'l2_rqsts.demand_data_rd_hit',
    'l2_rqsts.demand_data_rd_miss',
    'l2_rqsts.rfo_hit',
    'l2_rqsts.rfo_miss',
    'l2_lines_in.all',
    'l2_lines_out.silent',
    'l2_lines_out.non_silent',
    'longest_lat_cache.reference',
    'longest_lat_cache.miss',
    'mem_load_retired.l1_hit',
    'mem_load_retired.l1_miss',
    'mem_load_retired.l2_hit',
    'mem_load_retired.l2_miss',
    'mem_load_retired.l3_hit',
    'mem_inst_retired.any',
    'mem_inst_retired.all_loads',
    'mem_inst_retired.all_stores',
    'mem_inst_retired.split_stores',
    'mem_inst_retired.lock_loads',

    # ===== Branch =====
    'br_inst_retired.all_branches',
    'br_inst_retired.conditional',
    'br_inst_retired.near_taken',
    'br_inst_retired.not_taken',
    'br_misp_retired.all_branches',
    'br_misp_retired.conditional',
    'br_misp_retired.near_taken',

    # ===== TLB / ICache =====
    'itlb-load-misses',
    'itlb.itlb_flush',
    'itlb_misses.walk_completed',
    'itlb_misses.walk_completed_4k',
    'itlb_misses.walk_completed_2m_4m',
    'dtlb-load-misses',
    'dtlb-store-misses',
    'dtlb-loads',
    'dtlb-stores',
    'dtlb_load_misses.walk_active',
    'dtlb_load_misses.walk_pending',
    'dtlb_load_misses.walk_completed',
    'dtlb_load_misses.walk_completed_4k',
    'dtlb_load_misses.walk_completed_2m_4m',
    'icache_64b.iftag_hit',
    'icache_64b.iftag_miss',
    'icache_64b.iftag_stall',
    'icache_16b.ifdata_stall',

    # ===== Machine Clears / Recovery =====
    'machine_clears.count',
    'int_misc.clears_count',
    'int_misc.recovery_cycles',
    'int_misc.recovery_cycles_any',
    'int_misc.clear_resteer_cycles',
    'memory_disambiguation.history_reset',
    'other_assists.any',

    # ===== Frontend / IDQ =====
    'idq.ms_cycles',
    'idq.ms_uops',
    'idq.dsb_uops',
    'idq.dsb_cycles',
    'idq.mite_cycles',
    'idq.mite_uops',
    'idq_uops_not_delivered.core',
    'frontend_retired.dsb_miss',
    'frontend_retired.latency_ge_1',
    'frontend_retired.latency_ge_2'
      
    # Add more events if needed
]

# --------------------------------------------------------
# 2. CLEAN RUN (baseline without errors)
# --------------------------------------------------------
def perform_run(batch_id, num_runs, max_counter, event_name_arr):
    num_loops_needed = math.ceil(len(event_name_arr) / max_counter)
    base_name = f"{output_dir}/sample_3_mantissaFlip1_0.00_0.{batch_id + 1}.mtx_1"
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
                #f"./crs_matmult --matrix {matrix}"
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
                #f"./crs_matmult --matrix {matrix_file}"
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
    os.path.join(input_dir, f[:-4])
    for f in os.listdir(input_dir)
    if f.startswith("sample_3_mantissaFlip1_") and f.ends
])

# Run CLEAN (baseline) experiments
for batch_id2 in range(100):
    perform_run(batch_id2, 1, max_counter, event_name_arr)

# Run ERROR (corrupted) experiments
for matrix_file in input_files:
    for batch_id in range(100):
        perform_run_error(matrix_file, batch_id, 1, max_counter, event_name_arr)
