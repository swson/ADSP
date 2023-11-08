#! /usr/bin/bash

matrix_list=(
		dense
		3dtube
		crystk03
		crystk02
		gupta1
		raefsky4
		ct20stif
		bcsstk35
		vibrobox
		pwt
		finan512
		saylr4
		penta\\\\_diagonal
		bcspwr10
		shallow\\\\_water2
		LFAT5000
		1138\\\\_bus
		494\\\\_bus
		largetridiagonal
		Chem97Zt
		bcsstm39
	)

echo -e "matrix\tmean\terrlo\terrhi"
for m in ${matrix_list[@]}; do
	grep ${m} ${1}
done
