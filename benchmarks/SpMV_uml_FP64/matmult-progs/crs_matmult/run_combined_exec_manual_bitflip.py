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
output_dir = "output_sample_bit51/out_sample_bit51_simple_500pmc"

#matrix = "input/bfwb62_bitflip_MSB/bfwb62.mtx.crs"
#input_dir = "input/bfwb62_bitflip_MSB"
#output_dir = "output_1/out_bfwb62_bitflip_MSB_1_manual"
os.makedirs(output_dir, exist_ok=True)

# --------------------------------------------------------
# 1. List of hardware events to monitor (edit as needed)
# --------------------------------------------------------
event_name_arr = [
    'unc_cha_txr_horz_nack.bl_bnc',
'unc_cha_txr_horz_nack.ak_bnc',
'unc_m_act_count.byp',
'unc_m_wr_cas_rank0.bank11',
'memory_disambiguation.history_reset',
'unc_m_wr_cas_rank0.bank12',
'unc_cha_rxr_inserts.iv_bnc',
'itlb-load-misses',
'unc_cha_llc_victims.total_m',
'unc_cha_llc_victims.total_s',
'unc_cha_vert_ring_bl_in_use.dn_odd',
'unc_m_wr_cas_rank0.allbanks',
'dtlb_load_misses.walk_completed_2m_4m',
'unc_cha_rxr_bypass.ad_bnc',
'arith.divider_active',
'unc_m_wr_cas_rank1.bank10',
'unc_cha_txr_horz_inserts.ad_bnc',
'llc_misses.mem_write',
'uops_executed.x87',
'unc_m_act_count.wr',
'unc_m_wr_cas_rank0.bank0',
'unc_cha_txr_horz_bypass.ad_bnc',
'unc_cha_txr_horz_cycles_ne.iv_bnc',
'unc_cha_requests.writes_local',
'unc_m_wpq_inserts',
'unc_m2m_write_tracker_cycles_ne.ch0',
'itlb_misses.walk_completed_4k',
'unc_cha_core_snp.evict_one',
'unc_cha_ring_sink_starved_vert.iv',
'unc_cha_txr_vert_occupancy.ak_ag1',
'itlb_misses.walk_completed',
'unc_cha_txr_horz_occupancy.ad_bnc',
'unc_m2m_write_tracker_cycles_ne.ch1',
'unc_cha_txr_horz_bypass.iv_bnc',
'unc_m_wpq_cycles_ne',
'unc_cha_txr_vert_inserts.ad_ag0',
'unc_cha_txr_vert_cycles_ne.bl_ag1',
'unc_cha_txr_horz_ads_used.bl_crd',
'unc_m2m_txc_ak_cycles_ne.all',
'unc_m_wr_cas_rank1.bankg0',
'unc_cha_txr_vert_bypass.ak_ag1',
'unc_cha_txr_horz_inserts.iv_bnc',
'unc_cha_txr_vert_occupancy.ad_ag0',
'unc_cha_llc_victims.remote_s',
'unc_cha_rxr_inserts.bl_crd',
'msr:write_msr',
'unc_m3upi_ag1_ad_crd_acquired.tgr3',
'unc_cha_txr_vert_occupancy.bl_ag1',
'unc_m_wr_cas_rank1.bank4',
'unc_cha_llc_victims.remote_all',
'unc_cha_txr_horz_bypass.ak_bnc',
'unc_cha_rxr_bypass.bl_crd',
'unc_cha_txr_vert_ads_used.bl_ag1',
'unc_cha_txr_vert_bypass.bl_ag1',
'unc_cha_rxr_bypass.iv_bnc',
'unc_cha_llc_victims.total_e',
'unc_cha_llc_victims.local_s',
'unc_m3upi_ag0_ad_crd_acquired.tgr3',
'unc_cha_txr_vert_occupancy.bl_ag0',
'unc_cha_ag1_bl_crd_occupancy.tgr2',
'unc_m3upi_txr_vert_bypass.ak_ag1',
'unc_cha_rxc_inserts.irq',
'unc_cha_txr_vert_occupancy.ak_ag0',
'mem_inst_retired.stlb_miss_stores',
'icache_64b.iftag_stall',
'dtlb_load_misses.walk_active',
'unc_m2m_txc_ak_occupancy.wrcmp',
'x86_fpu:x86_fpu_regs_activated',
'itlb_misses.walk_completed_2m_4m',
'msr:read_msr',
'unc_m2m_txc_ak_sideband.wr',
'unc_m2m_txc_ak_occupancy.wrcrd',
'ld_blocks.no_sr',
'dtlb_load_misses.walk_completed',
'idq.ms_cycles',
'l2_rqsts.pf_hit',
'unc_m2m_rxc_bl_occupancy',
'unc_m2m_txr_vert_occupancy.ak_ag0',
'unc_cha_ag1_bl_credits_acquired.tgr0',
'dtlb-load-misses',
'dtlb_store_misses.stlb_hit',
'l2_rqsts.all_pf',
'unc_m2m_rxc_bl_inserts',
'timer:hrtimer_start',
'sw_prefetch_access.any',
'cpu-clock',
'unc_m2m_rxc_bl_cycles_ne',
'offcore_requests_outstanding.demand_code_rd',
'sched:sched_stat_runtime',
'unc_cha_rxr_crd_starved.bl_crd',
'unc_m2m_txc_ak_cycles_ne.wrcrd',
'unc_cha_txr_vert_inserts.iv',
'unc_cha_txr_horz_occupancy.iv_bnc',
'resource_stalls.sb',
'dtlb_load_misses.stlb_hit',
'unc_cha_txr_horz_ads_used.bl_bnc',
'idq.ms_mite_uops',
'sw_prefetch_access.t0',
'unc_cha_rxr_busy_starved.bl_crd',
'offcore_requests_outstanding.all_data_rd',
'offcore_requests_outstanding.demand_data_rd',
'br_misp_retired.ret',
'idq.ms_uops',
'unc_cha_txr_vert_cycles_ne.iv',
'offcore_requests_outstanding.cycles_with_demand_data_rd',
'unc_cha_xsnp_resp.core_rsp_hitfse',
'exe_activity.exe_bound_0_ports',
'rseq:rseq_update',
'unc_upi_txl0p_power_cycles_ll_enter',
'unc_cha_txr_horz_bypass.bl_bnc',
'l1d_pend_miss.pending_cycles',
'offcore_requests_outstanding.cycles_with_data_rd',
'cycle_activity.stalls_l2_miss',


      
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
    os.path.join(input_dir, f)
    for f in os.listdir(input_dir)
    if f.startswith("sample_3_mantissaFlip1_") and f.endswith(".crs")
])

# Run CLEAN (baseline) experiments
for batch_id2 in range(100):
    perform_run(batch_id2, 1, max_counter, event_name_arr)

# Run ERROR (corrupted) experiments
for matrix_file in input_files:
    for batch_id in range(100):
        perform_run_error(matrix_file, batch_id, 1, max_counter, event_name_arr)
