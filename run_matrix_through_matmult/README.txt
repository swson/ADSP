Convert mtx formatted matrices into crs formatted matrices
----------------------------------------------------------

    Perform this step if your baseline and error-injected matrices aren't in CRS format.

    Place all of your mtx formatted matrices in the folder labeled "matrix_data_mtx_format".

    In the terminal, type: "python3 multiple_mtx2crs.py". This will convert all of the error-injected as well as baseline matrices in this directory, convert them to CRS format, and store them in matmult-progs/crs_matmult/matrix_data_crs_format.


Run CRS matrices through matmult and collect perf stat results
--------------------------------------------------------------

    Navigate to matmult-progs/crs_matmult

    Type "make" in your terminal

    Open the file "perform_runs_on_crs_matrices.py" in order to change the following global variables:

        - num_runs, which determines the number of runs to perform on each matrix within the matrix_data_crs_format

        - num_counters, which is determined by the microarchitecture you are using. Each architecture has a maximum number of counters (i.e. hardware events) that you can monitor at a given time without incurring more management and associated system overhead.


    Once these settings have been updated to reflect your needs, navigate to your terminal and type "python3 perform_runs_on_crs_matrices.py"

    This program will:

        - Run perf list to get a list of all available hardware counters for your microarchitecture

        - Sanitize this output to just focus on events that have the "Event Name" key

        - Take this list of available event counters and break them up into groups of max_counters for your given system.

        - For each event group that you can monitor at a given time, you run one matrix from matrix_data_crs_format through your matrix multiplication while running perf stat to monitor this current event group's metrics. This process is repeated until all event groups have been monitored for this given matrix. This process is then repeated for run_num times. Then a new matrix from matrix_data_crs_format is loaded in and follows the process outlined above untill all matricies in matrix_data_crs_format have been processed.

        - This program also creates directories with aggregate run data files for each matrix.



Miscellaneous files
-------------------
    remove_json_files_for_testing.py is a utility file to get rid of automated JSON files if they are created in the wrong directory.
