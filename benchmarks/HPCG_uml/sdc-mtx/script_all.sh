#!/bin/bash

# Ensure PMU hardware counters are accessible
sudo sysctl -w kernel.perf_event_paranoid=-1 > /dev/null 2>&1

BIN=$(realpath hpcg-3.1/build/bin/xhpcg)

if [ ! -f "$BIN" ]; then
  echo "Error: xhpcg binary not found at: $BIN"
  exit 1
fi

# Set output directory to inference/raw relative to current script location
SCRIPT_DIR=$(dirname "$(realpath "$0")")
OUT="$SCRIPT_DIR/inference/raw/grid-494"

mkdir -p "$OUT"
cd "$OUT" || exit 1

# Phase 1: Fixed error/injection rate, repeated 100 times
FIXED_ERR_RATE=0.0
FIXED_INJ_RATE=0.0

for i in $(seq 0 99); do
  echo "Running (Phase 1) with Error rate = ${FIXED_ERR_RATE}, Injection rate = ${FIXED_INJ_RATE}, test = ${i}"

  sudo HPCG_PMU_MODE=timeseries \
       HPCG_PMU_INTERVAL_MS=10 \
       HPCG_PMU_OUTFILE="$OUT/pmu_ts_${i}.csv" \
       HPCG_ERR_RATE=$FIXED_ERR_RATE \
       HPCG_INJ_RATE=$FIXED_INJ_RATE \
       HPCG_TEST_ID=$i \
       HPCG_MATRIX_PATH="$SCRIPT_DIR/inference/494_bus.mtx" \
       LD_LIBRARY_PATH="$SCRIPT_DIR/libpmu":/usr/local/lib \
       $BIN 494 494 1
done

# Phase 2: Varying error/injection rate, one test per config
i=100
for ERR_RATE in $(seq 0.1 0.1 1.0); do
  for INJ_RATE in $(seq 0.01 0.01 0.10); do
    echo "Running (Phase 2) with Error rate = ${ERR_RATE}, Injection rate = ${INJ_RATE}, test = ${i}"

    timeout 30s sudo HPCG_PMU_MODE=timeseries \
         HPCG_PMU_INTERVAL_MS=10 \
         HPCG_PMU_OUTFILE="$OUT/pmu_ts_${i}.csv" \
         HPCG_ERR_RATE=$ERR_RATE \
         HPCG_INJ_RATE=$INJ_RATE \
         HPCG_TEST_ID=$i \
         HPCG_MATRIX_PATH="$SCRIPT_DIR/inference/494_bus.mtx" \
         LD_LIBRARY_PATH="$SCRIPT_DIR/libpmu":/usr/local/lib \
         $BIN 494 494 1

    ((i++))
  done
done


