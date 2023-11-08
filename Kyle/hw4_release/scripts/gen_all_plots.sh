
gen_plot() {
cat << EOF
		\begin{subfigure}[b]{0.45\columnwidth}
		\centering
		\begin{tikzpicture}
			\begin{axis}[
					xtick={1,2},
					xticklabels={TJDS, CRS},
					boxplot/draw direction=y,
					width=\columnwidth,
					height=2in,
				]

				\import{../plot_data/tjds/}{${1}_plot_data.tex}
				\import{../plot_data/crs/}{${1}_plot_data.tex}
			\end{axis}
		\end{tikzpicture}
		\caption{Results for \texttt{${1}} matrix.}
		\end{subfigure}
EOF
}

for m in ${@}; do
	gen_plot ${m}
done
