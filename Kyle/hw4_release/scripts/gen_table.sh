#/usr/bin/bash

gen_table_entry() {
cat << EOF
	\begin{longtable}{lXcc}
		\toprule
		\textbf{Matrix} & \textbf{Parameter} & \textbf{CRS Result} &
		\textbf{TJDS Result} \\\\
		\midrule
		\endhead
EOF
}

gen_table_footer() {
cat << EOF
		\bottomrule
		\end{longtable}
EOF
}

gen_table() {
cat << EOF
		\multirow{8}{*}{${1}}
		& Iterations & \multicolumn{2}{c}{1000} \\\\
		& Non-zero Elements & \multicolumn{2}{c}{${14}} \\\\
		& Timing Q0 & ${2} & ${8} \\\\
		& Timing Q1 & ${3} & ${9} \\\\
		& Timing Q2 & ${4} & ${10} \\\\
		& Timing Q3 & ${5} & ${11} \\\\
		& Timing Q4 & ${6} & ${12} \\\\
		& FLOPS & ${7} &  ${13} \\\\
		\midrule
EOF
}

gen_table_entry
for m in ${@}; do
	CRS_Q0=$(grep "lower whisker" ../plot_data/crs/${m}_plot_data.tex \
		| cut -d '=' -f 2 | tr -d ',')
	CRS_Q1=$(grep "lower quartile" ../plot_data/crs/${m}_plot_data.tex \
		| cut -d '=' -f 2 | tr -d ',')
	CRS_Q2=$(grep "median" ../plot_data/crs/${m}_plot_data.tex \
		| cut -d '=' -f 2 | tr -d ',')
	CRS_Q3=$(grep "upper quartile" ../plot_data/crs/${m}_plot_data.tex \
		| cut -d '=' -f 2 | tr -d ',')
	CRS_Q4=$(grep "upper whisker" ../plot_data/crs/${m}_plot_data.tex \
		| cut -d '=' -f 2 | tr -d ',')
	TJDS_Q0=$(grep "lower whisker" ../plot_data/tjds/${m}_plot_data.tex \
		| cut -d '=' -f 2 | tr -d ',')
	TJDS_Q1=$(grep "lower quartile" ../plot_data/tjds/${m}_plot_data.tex \
		| cut -d '=' -f 2 | tr -d ',')
	TJDS_Q2=$(grep "median" ../plot_data/tjds/${m}_plot_data.tex \
		| cut -d '=' -f 2 | tr -d ',')
	TJDS_Q3=$(grep "upper quartile" ../plot_data/tjds/${m}_plot_data.tex \
		| cut -d '=' -f 2 | tr -d ',')
	TJDS_Q4=$(grep "upper whisker" ../plot_data/tjds/${m}_plot_data.tex \
		| cut -d '=' -f 2 | tr -d ',')
	NNZ=$(grep ${m} ../mat/symm_data | cut -d ' ' -f 2)
	CRS_FLOP=$(echo "(2*${NNZ})/${CRS_Q2}" | bc -l)
	TJDS_FLOP=$(echo "(2*${NNZ})/${TJDS_Q2}" | bc -l)
	gen_table ${m} ${CRS_Q0} ${CRS_Q1} ${CRS_Q2} ${CRS_Q3} ${CRS_Q4} \
				${CRS_FLOP} \
			${TJDS_Q0} ${TJDS_Q1} ${TJDS_Q2} ${TJDS_Q3} ${TJDS_Q4} \
				${TJDS_FLOP} ${NNZ}
done
gen_table_footer
