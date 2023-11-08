#! /usr/bin/bash

wd=$(cd $(dirname ${0}); pwd -P)
run_list=({crs,tjds}_matmult{,_omp})

for re in ${run_list[@]}; do
	for f in ${wd}/../results/${re}/*; do
		[[ -d ${f} ]] && grep "computational time:" ${f}/* | \
				cut -d ':' -f 3 | ${wd}/cycles2sec.py | \
				${wd}/genflopspoint.py -m ${f##*/}
	done > ${wd}/../plot_data/${re}_flops
done 
