#!/bin/bash

BIN=$(realpath hpcg-3.1/build/bin/xhpcg)

if [ ! -f "$BIN" ]; then
  echo "Error: xhpcg binary not found at: $BIN"
  exit 1
fi

# Set output directory to inference/raw relative to current script location
SCRIPT_DIR=$(dirname "$(realpath "$0")")

# Phase 1: Fixed error/injection rate, repeated 100 times
FIXED_ERR_RATE=0.0
FIXED_INJ_RATE=0.0

for ((i = 3; i < 5; i += 1)); do
    G=$((2 ** $i))
    OUT="$SCRIPT_DIR/inference/raw/grid-$G"
    mkdir -p $OUT && cd $OUT || exit 1

    for k in $(seq 0 99); do
	echo "Grid size = ${G}, Error rate = ${FIXED_ERR_RATE}, Injection rate = ${FIXED_INJ_RATE}, test = ${k}"
	sudo HPCG_ERR_RATE=$FIXED_ERR_RATE \
	     HPCG_INJ_RATE=$FIXED_INJ_RATE \
	     HPCG_TEST_ID=$k \
	     LD_LIBRARY_PATH=/usr/local/lib:$SCRIPT_DIR/libpmu \
             $BIN $G $G $G

    done


    # Phase 2: Varying error/injection rate, one test per config
    k=100

    for ERR_RATE in $(seq 0.1 0.1 1.0); do
        for INJ_RATE in $(seq 0.01 0.01 0.10); do
            echo "Grid size = ${G}, Error rate = ${ERR_RATE}, Injection rate = ${INJ_RATE}, test = ${k}"
            sudo HPCG_ERR_RATE=$ERR_RATE \
                 HPCG_INJ_RATE=$INJ_RATE \
                 HPCG_TEST_ID=$k \
                 LD_LIBRARY_PATH=/usr/local/lib:$SCRIPT_DIR/libpmu \
                 $BIN $G $G $G

            ((k++))
        done
    done
done
