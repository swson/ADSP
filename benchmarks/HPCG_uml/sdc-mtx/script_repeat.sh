#!/bin/bash

BIN=$(realpath hpcg-3.1/build/bin/xhpcg)

if [ ! -f "$BIN" ]; then
  echo " Error: xhpcg binary not found at: $BIN"
  exit 1
fi


ERR_RATE=0.0
INJ_RATE=0.0

OUT=~/Grid-494
mkdir -p $OUT
cd $OUT

for i in $(seq 0 99); do
    
    echo "Running with Error rate = ${ERR_RATE}, Injection rate = ${INJ_RATE}, test = ${i}"

    sudo HPCG_ERR_RATE=$ERR_RATE \
	 HPCG_INJ_RATE=$INJ_RATE \
	 HPCG_TEST_ID=$i \
	 HPCG_MATRIX_PATH=/users/mchoi/adsp/sdc-inference/inference/494_bus.mtx \
	 LD_LIBRARY_PATH=/usr/local/lib:/users/mchoi/adsp/sdc-inference/libpmu \
	 $BIN 494 494 1
done
