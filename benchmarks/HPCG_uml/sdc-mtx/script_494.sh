#!/bin/bash

BIN=$(realpath hpcg-3.1/build/bin/xhpcg)

if [ ! -f "$BIN" ]; then
  echo " Error: xhpcg binary not found at: $BIN"
  exit 1
fi

OUT=~/grid-494
mkdir -p $OUT
cd $OUT


for ERR_RATE in $(seq 0.1 0.1 1.0); do
  for INJ_RATE in $(seq 0.01 0.01 0.10); do
    echo "Running with Error rate = ${ERR_RATE}, Injection rate = ${INJ_RATE}"

    timeout 30s sudo env HPCG_ERR_RATE=$ERR_RATE \
	 HPCG_INJ_RATE=$INJ_RATE \
	 HPCG_MATRIX_PATH=/users/mchoi/adsp/sdc-inference/inference/494_bus.mtx \
	 LD_LIBRARY_PATH=/usr/local/lib:/users/mchoi/adsp/sdc-inference/libpmu \
	 $BIN 494 494 1
  done
done
