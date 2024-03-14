import os
import json
import csv 
import subprocess
import time
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
import math

os.chdir("..")
project_home = os.getcwd()  #Changing path from python_files folder to project home directory

matrix_name = "494_bus"
file_type = "crs"
file_composition = "non_zero"
microarch_directory_name = "skylake"  # will become list of microarch 


path_to_baseline_file = os.path.join(project_home, "matrix_directory",matrix_name,file_type,"baseline_matrix_uncorrupted")
path_to_corrupted_files = os.path.join(project_home,"matrix_directory",matrix_name,file_type,file_composition )

path_to_exe = os.path.join(project_home,"hw4_release","matmult-progs","crs_matmult")


num_runss = 100


############################################ Function declarations


def get_event_names(path_to_json_file,event_file):

    event_name_arr = []

    #path_to_json_file = os.path.join(project_home,event_file)

    with open(path_to_json_file) as f:              # absolute path to json file
            contents = json.load(f)

    for c in contents:                      # data in json file is a list of dictionaries

        event_name_arr.append( c["EventName"] ) # will be used for graphing later on

    #print(event_name_arr,"\n")
    print("length of event_name_arr: ", len(event_name_arr) )
    print("\n")
    return event_name_arr





def get_matrix_file_names(path_to_baseline_file,path_to_corrupted_files):

    matrix_file_names_list = os.listdir(path_to_baseline_file) + os.listdir(path_to_corrupted_files)    # Joining the two lists together. BASELINE SHOULD ALWAYS BE FIRST ELEMENT

    return sorted(matrix_file_names_list)   # will be file_name.extension, where extension != csv. ex) if using crs files, all files end in .crs in this list









def single_run(matrix_file_names_list, event_name_arr, max_counter,path_to_data,event_name):

        print("matrix_file_names_list: ", matrix_file_names_list)
        print()
        print()


        print("path to data: ", path_to_data)
        print()

         
        for i  in range( len(matrix_file_names_list) ):		               # go through all of the matrix files being used one by one


                if ( i == 0 ):

                        os.chdir(path_to_baseline_file)
                        
                        #print("current path: " + path_to_baseline_file)
                        #print()

                        subprocess.run( ["cp " + matrix_file_names_list[i] + " " + path_to_exe], shell = True )	    # copy matrix being tested into exe directory

                        

                else:
                        os.chdir(path_to_corrupted_files)
                        #print("current path: " + path_to_corrupted_files)
                        #print()
                        
                        subprocess.run( ["cp " + matrix_file_names_list[i] + " " + path_to_exe], shell = True )	    # copy matrix being tested into exe directory


        os.chdir(path_to_exe)		# Changing from the python files directory this program was ran from into the directory where the execuatble is



	        

        # how many loops it will take to get through all possible data given that data will be split up into divisions of max_counter

        num_loops_needed = math.ceil( len(event_name_arr) / max_counter )        # take all possible y values and divide them into groups of max_counter.

        event_name_string =""	

        start = 0
        end = 0 


        for total_groups_created in range(1, (num_loops_needed + 1) ): 

                
              

                #path_to_data = os.path.join(path_to_data,dir_name)


                if ( total_groups_created * max_counter ) > len(event_name_arr):

                        end = end + len(event_name_arr) - start                                  

                else:
                        end = ( total_groups_created * max_counter )



                
                for j in range(start,end):            # division data window is the space between these running start and end values


                        if j == start:             # creating event name string that will be passed to perf stat command, containing max_counter event_names 

	                        event_name_string = event_name_string + event_name_arr[j]
	                        

                        else:
	                        event_name_string = event_name_string +","+ event_name_arr[j]



                data_window_event_name_arr_subset = event_name_string.split(',')



                for matrix in ( matrix_file_names_list ):		               # go through all of the matrix files being used one by one

                
                        print("event_name_string: ", event_name_string)
                        print()


	                

                        for i in range(num_runss + 1):
                                subprocess.run( [f"sudo perf stat -x , -o {matrix}_{event_name}_csv_file_{i} -e {event_name_string} ./crs_matmult --matrix {matrix}  --output {matrix}_{event_name}_output_run_{i}.txt"], shell = True) #crs_matmult_omp

	                



               

                event_name_string =""

                start = end

	        
	        
	        
	        

		        
        for remove_matrix_from_exe_dir in matrix_file_names_list:	
	        try:
		        os.remove( remove_matrix_from_exe_dir )
		        print( remove_matrix_from_exe_dir , " removed successfully")

	        except OSError as error:
	        
		        print(error)
		        print("file path can not be removed")



		
		
	
	
	
	
"""
	
def create_data_directories(path_to_data, trial_name):

	original_working_directory = os.getcwd()
	
	os.chdir(path_to_data)
	
	subprocess.run( ["sudo mkdir " + trial_name], shell = True )
	
	#subprocess.run( ["cd -P"+ trial_name], shell = True )
	
	os.chdir(trial_name)
	
	subprocess.run( ["sudo mkdir " + "single_run "], shell = True )
	
	os.chdir("single_run")
	
	subprocess.run( ["sudo mkdir csv_files"], shell = True)
	
	#os.chdir("..")
	
	#os.chdir("multi_run")
	
	#subprocess.run( ["sudo mkdir csv_files"], shell = True)
	
	#os.chdir("..")
	
	os.chdir(original_working_directory)
	
"""	
	

	
	
########################################################################################################################################################### Main








max_counter = 4

num_runs = 2

run_type = "single_run"


event_list = ["hw","sw","cache","pmu"]

temp_path = os.path.join(project_home,"x86",microarch_directory_name)

#path_to_json_file = os.path.join(project_home,"x86",microarch_directory_name, event_file)

for event_name in event_list:
    
    os.chdir(temp_path)

    subprocess.run( ["sudo perf list -j "+ event_name + " > perf_list_output_"+event_name+".json"] , shell = True)

    event_file = "perf_list_output_"+event_name+".json"
    
    path_to_json_file = os.path.join(temp_path, event_file)

    os.chdir(project_home)


    event_name_arr = get_event_names(path_to_json_file,event_file)

    #event_name_arr = event_name_arr[:8]	# just doing this for testing purposes. Remove later



    matrix_file_names_list = get_matrix_file_names(path_to_baseline_file,path_to_corrupted_files)


    trial_name = event_file

    path_to_data = os.path.join(project_home,"data",matrix_name)			#trial_name,run_type,"csv_files")

    #create_data_directories(path_to_data, trial_name)


    path_to_data = os.path.join(project_home,"data",matrix_name, trial_name, run_type, "csv_files")




    single_run(matrix_file_names_list, event_name_arr, max_counter,path_to_data,event_name)












