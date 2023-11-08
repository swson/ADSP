#! /usr/bin/bash

function run_all_tjds() {
	for m in ${MATRIX_LIST[@]}; do
		[[ -e results/${1}/${m} ]] && rm -r "results/${1}/${m}"
		mkdir -p "results/${1}/${m}"
		if [ ! -e "mat_cache/tjds/${m}/${m}.tjds" ]; then
			echo "[-] caching ${m}..."
			mkdir -p "mat_cache/tjds/${m}"
			./mtx2tjds/mtx2tjds.py < mat/${m}/${m}.mtx \
					> mat_cache/tjds/${m}/${m}.tjds
		fi
		for (( i=1; i<=${3}; i++ )); do
			echo "  [$(date +'%Y-%m-%d %H:%M:%S')] running ${m} ${i}"
			${2} \
					./tjds_matmult/${1} < mat_cache/tjds/${m}/${m}.tjds \
					> "results/${1}/${m}/${m}_run_${i}"
		done
	done
}

function run_all_crs() {
	for m in ${MATRIX_LIST[@]}; do
		[[ -e results/${1}/${m} ]] && rm -r "results/${1}/${m}"
		mkdir -p "results/${1}/${m}"
		if [ ! -e "mat_cache/crs/${m}/${m}.crs" ]; then
			echo "[-] caching ${m}..."
			mkdir -p "mat_cache/crs/${m}"
			./mtx2crs/mtx2crs.py < mat/${m}/${m}.mtx \
					> mat_cache/crs/${m}/${m}.crs
		fi
		for (( i=1; i<=${3}; i++ )); do
			echo "  [$(date +'%Y-%m-%d %H:%M:%S')] running ${m} ${i}"
			${2} \
					./crs_matmult/${1} < mat_cache/crs/${m}/${m}.crs \
					> "results/${1}/${m}/${m}_run_${i}"
		done
	done
}

function build() {
	echo "[-] building ${1} (opts: ${2})"
	cd ${1}_matmult
	make clean && make ${2}
	cd ${WD}
}

MATRIX_LIST=($(cat mat/matrix_list))
ITER_COUNT=10
WD=$(pwd)

# echo "[+] TJDS sequential run..."
# build tjds
# run_all_tjds "tjds_matmult" "taskset -c 0" ${ITER_COUNT}

echo "[+] TJDS parallel run..."
build tjds openmp
run_all_tjds "tjds_matmult_omp" "" ${ITER_COUNT}

echo "[+] CRS sequential run..."
build crs
run_all_crs "crs_matmult" "taskset -c 0" ${ITER_COUNT}

echo "[+] CRS parallel run..."
build crs openmp
run_all_crs "crs_matmult_omp" "" ${ITER_COUNT}
