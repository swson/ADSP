#!/bin/bash

set -e

# Usage:
#   ./script_all.sh 494_bus 494
#   ./script_all.sh 662_bus 662
#   ./script_all.sh 1138_bus 1138
#
# Default:
#   MATRIX_NAME=494_bus
#   GRID_SIZE=494

MATRIX_NAME=${1:-494_bus}
GRID_SIZE=${2:-494}

# Ensure PMU hardware counters are accessible
sudo sysctl -w kernel.perf_event_paranoid=-1 > /dev/null 2>&1
sudo modprobe msr

SCRIPT_DIR=$(dirname "$(realpath "$0")")

BIN="$SCRIPT_DIR/hpcg-3.1/build/bin/xhpcg"
MATRIX_PATH="$SCRIPT_DIR/../../../data/datasets/SuiteSparse_matrices/${MATRIX_NAME}.mtx"
OUT="$SCRIPT_DIR/inference/raw/${MATRIX_NAME}"
LOG_OUT="$SCRIPT_DIR/inference/hpcg_logs/${MATRIX_NAME}"


if [ ! -f "$BIN" ]; then
  echo "Error: xhpcg binary not found at: $BIN"
  exit 1
fi

if [ ! -f "$MATRIX_PATH" ]; then
  echo "Error: matrix file not found at: $MATRIX_PATH"
  exit 1
fi

if [ ! -f "$SCRIPT_DIR/libpmu/libpmu.so" ]; then
  echo "Error: libpmu.so not found at: $LIBPMU_DIR/libpmu.so"
  exit 1
fi

mkdir -p "$OUT"

echo "=============================================="
echo "Matrix name:   $MATRIX_NAME"
echo "Grid size:     $GRID_SIZE"
echo "Matrix path:   $MATRIX_PATH"
echo "Output dir:    $OUT"
echo "Binary:        $BIN"
echo "=============================================="

mkdir -p "$LOG_OUT"
cd "$LOG_OUT" || exit 1

# Phase 1: Normal runs, repeated 100 times
FIXED_ERR_RATE=0.0
FIXED_INJ_RATE=0.0

for i in $(seq 0 99); do
  OUTFILE="$OUT/pmu_ts_${i}_${FIXED_ERR_RATE}_${FIXED_INJ_RATE}.csv"

  echo "Running Phase 1: test_id=${i}, error=${FIXED_ERR_RATE}, injection=${FIXED_INJ_RATE}"

  sudo -E env \
    HPCG_PMU_MODE=timeseries \
    HPCG_PMU_INTERVAL_MS=10 \
    HPCG_PMU_OUTFILE="$OUTFILE" \
    HPCG_ERR_RATE="$FIXED_ERR_RATE" \
    HPCG_INJ_RATE="$FIXED_INJ_RATE" \
    HPCG_TEST_ID="$i" \
    HPCG_MATRIX_PATH="$MATRIX_PATH" \
    LD_LIBRARY_PATH="$SCRIPT_DIR/libpmu":/usr/local/lib \
    "$BIN" "$GRID_SIZE" "$GRID_SIZE" 1
done

# Phase 2: Faulty runs, one test per error/injection config
i=100

for ERR_RATE in $(seq 0.1 0.1 1.0); do
  for INJ_RATE in $(seq 0.01 0.01 0.10); do
    OUTFILE="$OUT/pmu_ts_${i}_${ERR_RATE}_${INJ_RATE}.csv"

    echo "Running Phase 2: test_id=${i}, error=${ERR_RATE}, injection=${INJ_RATE}"

    timeout 30s sudo -E env \
      HPCG_PMU_MODE=timeseries \
      HPCG_PMU_INTERVAL_MS=10 \
      HPCG_PMU_OUTFILE="$OUTFILE" \
      HPCG_ERR_RATE="$ERR_RATE" \
      HPCG_INJ_RATE="$INJ_RATE" \
      HPCG_TEST_ID="$i" \
      HPCG_MATRIX_PATH="$MATRIX_PATH" \
      LD_LIBRARY_PATH="$SCRIPT_DIR/libpmu":/usr/local/lib \
      "$BIN" "$GRID_SIZE" "$GRID_SIZE" 1

    ((i++))
  done
done

echo "=============================================="
echo "All runs completed."
echo "Files saved under: $OUT"
echo "=============================================="
