#! /usr/bin/bash

MATRIX_LIST=($(cat mat/symmlist.all))
mkdir -p plot_data/{tjds,crs}
for m in ${MATRIX_LIST[@]}; do
	grep "computational time" results/tjds/${m}/${m}* | cut -d ':' -f 3 \
		| ./cycles2sec/cycles2sec.py | ./dataproc/dataproc.py \
		>  plot_data/tjds/${m}_plot_data.tex
done

for m in ${MATRIX_LIST[@]}; do
	grep "computational time" results/crs/${m}/${m}* | cut -d ':' -f 3 \
		| ./cycles2sec/cycles2sec.py | ./dataproc/dataproc.py \
		>  plot_data/crs/${m}_plot_data.tex
done
