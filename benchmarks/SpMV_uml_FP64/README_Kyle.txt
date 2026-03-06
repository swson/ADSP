In python_files you will find files for converting matricies from mtx format to crs format. Matricies need to be in crs format to be run by matrix multiplication program in matmult_progs. 

matmult_progs contains a program that will perform matrix multiplication on a given input matrix. We use matrix multiplication to represent a workload being performed on the system that we later use perf to monior. 

To run this program go to crs_matmult directory. Upload your matrix in crs format. 

To get a list of all hardware events for your system, install perf and once it is installed, type the following 
into the command line: perf list -o "list_of_all_hw_events.json" -j     to get a list of all the hardware event counters on your system in a json formatted file.

run make to get the crs_matmult program ready.

run 494_uncorrupted_runs.py to get 5 runs of the uncorrupted matrix each copied 100 times and stored in individual folders. 


remove_json_files_for_testint.py is a utility file to get rid of automated json files that are created in the wrong directory. 

 
