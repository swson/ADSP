
import os
import json
import csv
import subprocess

"""

want to go to directory where x86 data is located. Put this python program there. 

events that we are interested in: floating point, cache, branch predictor.

"""

#project_directory = "/home/kchai/Documents/current/current_research/professor_Son_research/code/11-1-23_code_modifications"

#"/home/kchai/Documents/current/current_research/professor_Son_research/misc/x86"

x86_arch_directory = "/home/kchai/src/git/linux/tools/perf/pmu-events/arch/x86/"


microarch_directory_name = "skylake"  # will become list of microarch 

event_file = "pipeline.json"

#"cache.json"   # this will eventually be a list of event names that I am interested in monitoring. 

#"pipeline.json"

#"floating-point.json"


executable_directory_baseline = "/home/kchai/Documents/current/current_research/professor_Son_research/hw4_release/crs_matmult" 

executable_name_baseline = "crs_matmult_omp"




file_name = os.path.join(x86_arch_directory,microarch_directory_name,event_file)





file2_name = os.path.join('.',"perf_list_output.txt")   # perf list > perf_list_output.txt .. file placed in cwd







#executable_directory_corrupted = "/home/kchai/Documents/current/current_research/professor_Son_research/hw4_release/crs_matmult" 

#executable_name_corrupted = "crs_matmult_omp"



output_log_file_baseline = "temp_shell_output_baseline.csv"

output_log_file_corrupted = "temp_shell_output_corrupted.csv"




event_name_arr = []
event_name_string =""

with open(file_name) as f:              # absolute path to json file
        contents = json.load(f)

for c in contents:                      # data in json file is a list of dictionaries
    event_name_arr.append( c["EventName"] )
    



with open(file2_name) as f2:            # perf list output file
    perf_list_content = f2.read()
    
    


    




event_name_string = ",".join(event_name_arr)




os.chdir(executable_directory_baseline)      # I go to the executable directory to run my subprocess command 

subprocess.run( ["sudo perf stat -x , -o " + output_log_file_corrupted + " -e " + event_name_string + " ./" + executable_name_baseline ], shell = True)




"""
*** Go Here This is where you are going to get your files now


~/src/git/linux/tools/perf/pmu-events/arch/x86/skylake


Now you don't have to filter your perf list results. 



https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git

"""




















