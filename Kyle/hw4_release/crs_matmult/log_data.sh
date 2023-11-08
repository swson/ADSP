#!/bin/bash


#mkdir results_1

cd results_1

#mkdir trial_1 trial_2

cd trial_1 

#touch pc_baseline.txt mat_baseline.txt mat_injected.txt

sudo perf stat -a -r 5 -e fp_arith_inst_retired.128b_packed_double,fp_arith_inst_retired.128b_packed_single,fp_arith_inst_retired.256b_packed_double,fp_arith_inst_retired.256b_packed_single,fp_arith_inst_retired.scalar_double,fp_arith_inst_retired.scalar_single sleep 1 >> pc_baseline.txt

sudo perf stat -a -r 5 -e fp_arith_inst_retired.128b_packed_double,fp_arith_inst_retired.128b_packed_single,fp_arith_inst_retired.256b_packed_double,fp_arith_inst_retired.256b_packed_single,fp_arith_inst_retired.scalar_double,fp_arith_inst_retired.scalar_single ./crs_matmult_omp >> mat_baseline.txt
