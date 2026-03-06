import os
import subprocess
import math
from pathlib import Path

# ======================
# CONFIGURATION
# ======================
max_counter = 4
batch_id2 = 0

matrix = "input_avg/bfwb782_1/crs/non_zero/bfwb782.mtx.crs"
input_dir = "input_avg/bfwb782_1/crs/non_zero"
output_dir = "output_point_gauss_all_avg/bfwb782_1"
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
'unc_cha_txr_vert_occupancy.iv',
'dsb2mite_switches.count',
'l1d_pend_miss.fb_full',
'unc_cha_txr_vert_inserts.ak_ag1',
'l2_rqsts.demand_data_rd_miss',
'dtlb_load_misses.walk_pending',
'mem_inst_retired.stlb_miss_loads',
'unc_cha_rxr_bypass.ak_bnc',
'unc_cha_txr_vert_cycles_ne.ad_ag0',
'offcore_requests_outstanding.cycles_with_demand_rfo',
'cycle_activity.cycles_l2_miss',
'unc_cha_xsnp_resp.core_rsps_fwdm',
'l1d_pend_miss.pending_cycles_any',
'kmem:kfree',
'unc_m2m_cms_clockticks',
'unc_m2m_clockticks',
'unc_cha_txr_vert_inserts.bl_ag1',
'cycle_activity.stalls_l1d_miss',
'unc_cha_rxr_occupancy.bl_crd',
'unc_cha_imc_writes_count.full',
'unc_m2m_vert_ring_iv_in_use.dn',
'unc_m2m_txc_ak_credits_acquired.cms0',
'l2_lines_out.silent',
'unc_m_wmm_to_rmm.low_thresh',
'partial_rat_stalls.scoreboard',
'unc_cha_xsnp_resp.any_rsp_hitfse',
'dtlb_load_misses.miss_causes_a_walk',
'dtlb-store-misses',
'unc_cha_xsnp_resp.core_rspi_fwdm',
'longest_lat_cache.miss',
'unc_cha_llc_victims.local_m',
'tlb:tlb_flush',
'unc_cha_xsnp_resp.any_rsps_fwdm',
'l1d_pend_miss.pending',
'l2_lines_out.non_silent',
'unc_m_dram_refresh.high',
'offcore_requests_outstanding.cycles_with_demand_code_rd',
'l2_rqsts.references',
'unc_cha_llc_victims.local_all',
'mem_load_retired.l3_hit',
'unc_upi_txl_flits.idle',
'unc_cha_rxr_bypass.bl_bnc',
'longest_lat_cache.reference',
'frontend_retired.dsb_miss',
'cycle_activity.cycles_l1d_miss',
'unc_cha_txr_horz_cycles_ne.ad_bnc',
'unc_m_cas_count.rd_wmm',
'l2_rqsts.code_rd_miss',
'l2_rqsts.pf_miss',
'unc_m_wpq_occupancy',
'l2_lines_out.useless_hwpf',
'inst_retired.nop',
'offcore_requests.demand_code_rd',
'l2_rqsts.miss',
'unc_m_major_modes.partial',
'l2_rqsts.rfo_miss',
'unc_cha_txr_vert_bypass.ad_ag0',
'offcore_requests.all_requests',
'offcore_requests.all_data_rd',
'idq.dsb_uops',
'unc_m_cas_count.rd_underfill',
'machine_clears.count',
'resource_stalls.any',
'int_misc.clears_count',
'idq.ms_switches',
'uops_executed.core_cycles_none',
'l2_trans.l2_wb',
'dtlb_store_misses.walk_completed_4k',
'unc_cha_xsnp_resp.any_rspi_fwdm',
'unc_m_wr_cas_rank1.bank15',
'unc_cha_txr_vert_inserts.ak_ag0',
'dtlb_store_misses.walk_pending',
'mem_inst_retired.split_stores',
'idi_misc.wb_upgrade',
'idq_uops_not_delivered.cycles_0_uops_deliv.core',
'ld_blocks.store_forward',
'topdown-recovery-bubbles',
'kmem:rss_stat',
'unc_m3upi_upi_peer_bl_credits_empty.vna',
'idq.all_dsb_cycles_4_uops',
'l2_rqsts.all_code_rd',
'int_misc.recovery_cycles',
'uops_retired.stall_cycles',
'kmem:kmem_cache_free',
'int_misc.recovery_cycles_any',
'br_misp_exec.all_branches',
'br_misp_retired.conditional',
'idq.ms_dsb_cycles',
'unc_cha_core_snp.core_one',
'uops_executed.stall_cycles',
'cache-references',
'idq_uops_not_delivered.cycles_le_1_uop_deliv.core',
'mem_load_retired.l1_miss',
'idq.all_dsb_cycles_any_uops',
'unc_cha_core_pma.c1_state',
'unc_m_wr_cas_rank1.bank14',
'rs_events.empty_end',
'unc_cha_txr_vert_inserts.bl_ag0',
'mem_load_l3_hit_retired.xsnp_none',
'icache_16b.ifdata_stall',
'dtlb_store_misses.walk_completed',
'unc_m3upi_txr_horz_cycles_full.ad_bnc',
'idq.dsb_cycles_any',
'offcore_requests.demand_data_rd',
'idq.dsb_cycles',
'unc_cha_core_snp.any_one',
'cpu_clk_thread_unhalted.ref_xclk_any',
'cpu_clk_thread_unhalted.ref_xclk',
'dtlb_load_misses.walk_completed_4k',
'unc_cha_upi_credits_acquired.bl_ncs',
'idq_uops_not_delivered.cycles_fe_was_ok',
'mem_inst_retired.lock_loads',
'branch-misses',
'uops_retired.total_cycles',
'l2_rqsts.code_rd_hit',
'unc_m3upi_vn1_no_credits.ncb',
'kmem:mm_page_alloc',
'rs_events.empty_cycles',
'unc_m_pre_count.wr',
'idq_uops_not_delivered.core',
'uops_dispatched_port.port_2',
'mem_load_retired.l2_hit',
'uops_issued.stall_cycles',
'faults',
'minor-faults',
'l2_rqsts.all_demand_data_rd',
'mem-stores',
'kmem:mm_page_free_batched',
'br_misp_exec.indirect',
'uops_issued.any',
'uops_dispatched_port.port_3',
'unc_iio_mask_match_and.bus0_bus1',
'unc_iio_mask_match_and.bus0',
'cpu_clk_thread_unhalted.one_thread_active',
'cpu_clk_unhalted.one_thread_active',
'frontend_retired.latency_ge_1',
'ild_stall.lcp',
'idq.dsb_cycles_ok',
'unc_iio_mask_match_and.bus1',
'l1-dcache-stores',
'dtlb-stores',
'unc_upi_clockticks',
'kmem:mm_page_free',
'idq.all_mite_cycles_any_uops',
'ref-cycles',
'idq.all_mite_cycles_4_uops',
'core_power.lvl0_turbo_license',
'mem_load_retired.l2_miss',
'cpu_clk_unhalted.thread_any',
'cpu_clk_unhalted.thread_p_any',
'cpu_clk_unhalted.thread_p',
'cpu_clk_unhalted.thread',
'uops_dispatched_port.port_1',
'exe_activity.4_ports_util',
'unc_m2m_tgr_bl_credits',
'cycle_activity.stalls_total',
'unc_m2m_tgr_ad_credits',
'unc_upi_txl0p_clk_active.rxq_bypass',
'unc_i_txc_bl_ncs_occupancy',
'int_misc.clear_resteer_cycles',
'uops_executed.thread',
'cycle_activity.stalls_mem_any',
'cpu_clk_unhalted.ref_xclk_any',
'cpu_clk_unhalted.ref_xclk',
'cpu_clk_unhalted.ref_tsc',
'cycles',
'cpu-cycles',
'unc_upi_rxl_flits.idle',
'sw_prefetch_access.prefetchw',
'mem_inst_retired.all_stores',
'dtlb-loads',
'br_misp_retired.all_branches_pebs',
'br_misp_retired.all_branches',
'l2_rqsts.rfo_hit',
'uops_dispatched_port.port_6',
'itlb.itlb_flush',
'topdown-slots-retired',
'unc_p_clockticks',
'unc_m3upi_txr_horz_cycles_full.bl_bnc',
'offcore_requests.demand_rfo',
'mem_inst_retired.any',
'l2_lines_in.all',
'unc_m3upi_m2_bl_credits_empty.iio4_ncb',
'uops_retired.retire_slots',
'mem_load_misc_retired.uc',
'uops_executed.cycles_ge_2_uops_exec',
'topdown-slots-issued',
'unc_iio_clockticks',
'pagemap:mm_lru_insertion',
'mem_inst_retired.all_loads',
'unc_m2m_txc_bl_credit_occupancy.cms1',
'unc_i_clockticks',
'unc_m_major_modes.write',
'unc_m2m_rpq_cycles_reg_credits.chn1',
'unc_m2m_rpq_cycles_reg_credits.chn0',
'inst_retired.prec_dist',
'task-clock',
'br_inst_retired.near_taken',
'bus-cycles',
'unc_upi_txl0p_clk_active.txq',
'unc_m2m_wpq_cycles_spec_credits.chn0',
'uops_executed.core_cycles_ge_3',
'frontend_retired.any_dsb_miss',
'unc_m2m_wpq_cycles_reg_credits.chn2',
'unc_m2m_wpq_cycles_spec_credits.chn1',
'idq.mite_cycles',
'unc_m2m_wpq_cycles_spec_credits.chn2',
'l1-dcache-load-misses',
'unc_m2m_wpq_cycles_reg_credits.chn1',
'unc_m2m_wpq_cycles_reg_credits.chn0',
'uops_executed.core_cycles_ge_4',
'branch-loads',
'l1-dcache-loads',
'l1d.replacement',
'inst_retired.any',
'l2_rqsts.demand_data_rd_hit',
'uops_executed.core',
'uops_executed.core_cycles_ge_1',
'icache_64b.iftag_hit',
'mem_load_retired.l1_hit',
'page-faults',
'br_inst_retired.not_taken',
'unc_cha_cms_clockticks',
'mmap_lock:mmap_lock_released',
'idq_uops_not_delivered.cycles_le_3_uop_deliv.core',
'mmap_lock:mmap_lock_acquire_returned',
'unc_m3upi_vn1_no_credits.ncs',
'br_inst_retired.all_branches_pebs',
'br_inst_retired.all_branches',
'uops_dispatched_port.port_5',
'instructions',
'unc_m_clockticks_f',
'unc_m3upi_vn1_no_credits.wb',
'idq.mite_uops',
'exe_activity.2_ports_util',
'unc_m3upi_vn1_no_credits.snp',
'br_inst_retired.cond_ntaken',
'unc_m3upi_m2_bl_credits_empty.iio5_ncb',
'unc_cha_clockticks',
'unc_u_clockticks',
'unc_m3upi_vn1_no_credits.rsp',
'uops_executed.cycles_ge_1_uop_exec',
'unc_m_clockticks',
'br_inst_retired.far_branch',
'mem_load_retired.fb_hit',
'uops_dispatched_port.port_4',
'uops_executed.core_cycles_ge_2',
'unc_m3upi_m2_bl_credits_empty.ncs',
'unc_m_power_cke_cycles.rank1',
'br_misp_retired.near_taken',
'unc_m_power_cke_cycles.rank0',
'uops_executed.cycles_ge_4_uops_exec',
'br_inst_retired.cond',
'br_inst_retired.conditional',
'duration_time',
'idq_uops_not_delivered.cycles_le_2_uop_deliv.core',
'uops_executed.cycles_ge_3_uops_exec',
'unc_iio_mask_match_or.not_bus0_not_bus1',
'unc_m2m_txc_bl_credit_occupancy.cms0',
'unc_u_racu_requests',
'unc_upi_txl0p_clk_active.cfg_ctl',
'icache_64b.iftag_miss',
'other_assists.any',
'branch-instructions',
'unc_m2m_txc_ak_credit_occupancy.cms0',
'llc-loads',
'branches',
'unc_m2m_txc_ak_credit_occupancy.cms1',
'exceptions:page_fault_user',
'unc_m_major_modes.read',
'l2_rqsts.all_demand_miss',
'unc_m2m_txc_ad_credit_occupancy',
'branch-load-misses',
'uops_retired.macro_fused',
'frontend_retired.latency_ge_2',
'uops_dispatched_port.port_0',
'unc_m3upi_clockticks',
'topdown-total-slots',
'unc_m3upi_cms_clockticks',
'unc_m2m_rpq_cycles_reg_credits.chn2',
'frontend_retired.latency_ge_2_bubbles_ge_3',
'unc_m2m_rpq_cycles_spec_credits.chn0',
'unc_m2m_rpq_cycles_spec_credits.chn1',
'unc_m2m_rpq_cycles_spec_credits.chn2',
'br_inst_retired.near_call',
'br_inst_retired.near_return',
'unc_m3upi_vn1_no_credits.req',
'dtlb_store_misses.walk_active',
'unc_m3upi_upi_peer_ad_credits_empty.vna',
'unc_iio_vtd_occupancy',
'unc_p_power_state_occupancy.cores_c0',
'decode.lcp',
'uops_issued.slow_lea',
'l2_rqsts.all_demand_references',
'uops_dispatched_port.port_7',
'exe_activity.3_ports_util',
'l1-icache-load-misses',
'unc_upi_rxl0_power_cycles',
'baclears.any',
'br_misp_retired.near_call',
'dtlb_store_misses.miss_causes_a_walk',
'unc_m2m_pkt_match.mc',
'unc_m2m_pkt_match.mesh',
'topdown-fetch-bubbles',
'exe_activity.1_ports_util',
'inst_decoded.decoders',
'unc_upi_txl0_power_cycles',
'mmap_lock:mmap_lock_start_locking',
'l2_rqsts.all_rfo',
'cycle_activity.cycles_mem_any',

  
    # Add more events if needed
]

# --------------------------------------------------------
# 2. CLEAN RUN (baseline without errors)
# --------------------------------------------------------
def perform_run(batch_id, num_runs, max_counter, event_name_arr):
    num_loops_needed = math.ceil(len(event_name_arr) / max_counter)
    base_name = f"{output_dir}/bfwb782_point_gauss_0.00_0.{batch_id + 1}.mtx_1"
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
    if f.startswith("bfwb782_point_gauss_") and f.endswith(".crs")
])

# Run CLEAN (baseline) experiments
for batch_id2 in range(100):
    perform_run(batch_id2, 1, max_counter, event_name_arr)

# Run ERROR (corrupted) experiments
for matrix_file in input_files:
    for batch_id in range(1):
        perform_run_error(matrix_file, batch_id, 1, max_counter, event_name_arr)
