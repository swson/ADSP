import os
import json
import csv
import subprocess
import time



########################################################################
# get all the crs files from the crs file directory
########################################################################

# want to pass these values in through a list coming from the main python program controlling all of the other python programs

matrix_name = "494_bus"
file_type = "crs"
file_composition = "non_zero"

path_to_corrupted_files = "../matrix_directory/" + matrix_name + "/" + file_type + "/" + file_composition		# This path relies on the current directory structure
list_of_corrupted_files = os.listdir(path_to_corrupted_files)

path_to_baseline_file = "../matrix_directory/" + matrix_name + "/" + file_type + "/baseline_matrix_uncorrupted"
baseline_file = os.listdir(path_to_baseline_file)

# creating list of list data structure containing all of the files. Baseline file is always at first index
list_of_all_files = []
list_of_all_files.append(baseline_file)
list_of_all_files.append(list_of_corrupted_files)


path_to_exe = "/hw4_release/crs_matmult"

path_to_program_files = "/home/kchai/Documents/current/current_research/professor_Son_research/code/project_demo/project_dir_template_demo/python_files" 

path_to_project_home = "/home/kchai/Documents/current/current_research/professor_Son_research/code/project_demo/project_dir_template_demo"

#files = ",".join(files) 


########################################################################
# json format parser
########################################################################


microarch_directory_name = "skylake"  # will become list of microarch 

event_file = "pipeline.json"

path_to_json_file = "../x86/"+ microarch_directory_name + "/" + event_file


""""
cache.json" 

"floating-point.json"

"memory.json"

"""


#getting all of the event names from the json file

event_name_arr = []
event_name_string =""

with open(path_to_json_file) as f:              # absolute path to json file
        contents = json.load(f)

for c in contents:                      # data in json file is a list of dictionaries
    event_name_arr.append( c["EventName"] ) # will be used for graphing later on


event_name_string = ",".join(event_name_arr)	# will be used in perf stat command






#copy over file from its directory, place it in executable directory, run executable on that file, remove file copy from exe directory

abs_path_to_exe = path_to_project_home + path_to_exe





#os.chdir(path_to_project_home)


os.chdir(path_to_baseline_file)

subprocess.run( ["cp " + list_of_all_files[0][0] + " " + abs_path_to_exe], shell = True )

os.chdir(abs_path_to_exe)



subprocess.run( ["make clean"], shell = True)
subprocess.run( ["make openmp"],shell = True)

subprocess.run( ["./crs_matmult_omp " + list_of_all_files[0][0] ],shell = True )






#subprocess.run( ["sudo perf stat -x , -o " + output_log_file_baseline + " -e " + event_name_string + " ./" + executable_name_baseline ], shell = True)




"""
if(p1.returncode == 0):
	p = subprocess.run( ["make openmp"],shell = True)
	
	if(p.returncode == 0):
		p2=subprocess.run( ["./crs_matmult_omp " + list_of_all_files[0][0] ],shell = True )
	

p2=subprocess.Popen( ["./crs_matmult_omp " + list_of_all_files[0][0] ],shell = True )
p2.wait()


os.chdir(executable_directory_baseline)      # I go to the executable directory to run my subprocess command 

subprocess.run( ["sudo perf stat -x , -o " + output_log_file_baseline + " -e " + event_name_string + " ./" + executable_name_baseline ], shell = True)

"""




























