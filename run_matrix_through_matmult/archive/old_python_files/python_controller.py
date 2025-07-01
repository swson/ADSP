"""

This program is most likely outdated and needs to be refactored. Provides boilerplate code.

This program will require you to update the path variables to reflect your own directory structure.
This program when plotting takes into account that different micro arch have different number of counters. In this case we have max of 4.
This means we can only monitor 4 events and must only pass 4 events to perf stat to prevent extra overhead per perf docs

"""


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







#event_file = "perf_list_output.json"  # will become list of microarch 
#

#os.chdir(path_to_json_file)
#subprocess.run( ["sudo perf list -j > " + event_file  ], shell = True)
#os.chdir(project_home)


#microarch_directory_name = perf_list_json_out.txt  # will become list of microarch 

#event_file_list = ["pipeline.json", "cache.json" , "floating-point.json","memory.json"] 
#event_file = event_file_list[0]



############################################ additional file paths that are subject to project directory structure

#path_to_json_file = os.path.join(project_home,"x86",microarch_directory_name, event_file)

#path_to_json_file = os.path.join(project_home,"python_files")#,microarch_directory_name)

path_to_baseline_file = os.path.join(project_home, "matrix_directory",matrix_name,file_type,"baseline_matrix_uncorrupted")
path_to_corrupted_files = os.path.join(project_home,"matrix_directory",matrix_name,file_type,file_composition )

path_to_exe = os.path.join(project_home,"hw4_release","matmult-progs","crs_matmult")

#os.path.join(project_home,"data",matrix_name,trial_name,run_type,"csv_files")

#1 gets paths to relevant files


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


#1 gets all of the perf event names from json file and stores them in list




def get_matrix_file_names(path_to_baseline_file,path_to_corrupted_files):

    matrix_file_names_list = os.listdir(path_to_baseline_file) + os.listdir(path_to_corrupted_files)    # Joining the two lists together. BASELINE SHOULD ALWAYS BE FIRST ELEMENT

    return sorted(matrix_file_names_list)   # will be file_name.extension, where extension != csv. ex) if using crs files, all files end in .crs in this list


#1 gets all of the matrix file names. Both baseline and uncorrupted

def parse_csv_get_x_vals( csv_file ):

	
	with open(csv_file) as f:

		matrix_x_vals = []

		line_reader = csv.reader(f)

		for row in line_reader:		# Each row is a list of string values

			if len(row) == 0:		# if the list is empty
				continue 

			elif row[0].startswith('#'):
				continue
		

			elif row[0].startswith('<'):
			
	 			matrix_x_vals.append(0)
	 			
			else:
				#matrix_x_vals.append( int( row[0] ) )	# matrix data stored in a list
                                matrix_x_vals.append( int( round(float(row[0] ) ) ) )

	return matrix_x_vals

#1 parses csv file to get x values for plotting


def plot_data( matrix_file_names_list, data_window_event_name_arr_subset, data_window_matrix_x_values, plot_info_string ):

		temp_y_values = data_window_event_name_arr_subset
		
		graph_dict = {}
	
		"""	
		print( "len(matrix_file_names_list) ", len(matrix_file_names_list) )
		print()
		print( "len(data_window_matrix_x_values) ", len(data_window_matrix_x_values) )
		print()
		"""	
		for i in range( len(matrix_file_names_list) -1 ):
		
			graph_dict[ matrix_file_names_list[i] ] = data_window_matrix_x_values[i]
			
		

		df =  pd.DataFrame( graph_dict, index =  temp_y_values )	

		ax = df.plot.barh(width = .85)	#width = .7 

		plt.xscale('log')

		plt.subplots_adjust(left=.3, right=.9, top=.9, bottom=0.05)
		
		plt.yticks(fontsize=9)

		ax.legend(loc='lower center', bbox_to_anchor=(0.35, 1.1),
		fancybox=True, shadow=True, ncol= len(matrix_file_names_list))

		#for container in ax.containers:

			#ax.bar_label(container,padding=5)

		plt.title("Event Monitored: " + event_file + " Group: " + plot_info_string)
		
		image_name = event_file + plot_info_string

		#plt.figure(figsize=(20,20))
		
		#plt.figure()
		#plt.rcParams['figure.figsize'] = [200, 200]
		#plt.tight_layout()
		
		plt.savefig( image_name, bbox_inches = 'tight')	#dpi = 200	#, pad_inches = 2	
		
		#plt.show()
		
		
		
		#1 plots data in bar chart
		
		
def local_aggr_csv( aggr_csv_file_name, column_labels, data_window_event_name_arr_subset, data_window_matrix_x_values):

#data_window_event_name_arr_subset, data_window_matrix_x_values, aggr_csv_file_name, column_labels):

	with open(aggr_csv_file_name,"a+") as f:
		
                f.write( column_labels + "\n" ) 

                if len(data_window_event_name_arr_subset) != len(data_window_matrix_x_values):
                    return
                else:

                        for i in range( len(data_window_event_name_arr_subset) ):

                                line_of_info = []

                                line_of_info.append( data_window_event_name_arr_subset[i] )


                        for j in range( len( data_window_matrix_x_values ) ):

                            line_of_info.append( str(data_window_matrix_x_values[j][i]) )


                        f.write( ",".join( line_of_info ) )

                        f.write("\n")
                    

#1 collects aggregate results for events
				
				
def create_global_aggr_csv(aggr_csv_file_name,column_labels):

	f =  open(aggr_csv_file_name,"w+")
	
	f.write( column_labels + "\n" ) 
	
	f.close()
					


				
				

def add_to_global_aggr_csv( aggr_csv_file_name, data_window_event_name_arr_subset, data_window_matrix_x_values):

	with open(aggr_csv_file_name,"a+") as f:
	        
	
                if len(data_window_event_name_arr_subset) != len(data_window_matrix_x_values):

                    return
                    
                else:
                        
                        for i in range( len(data_window_event_name_arr_subset) ):

	                        line_of_info = []

	                        line_of_info.append( data_window_event_name_arr_subset[i] )


	                        for j in range( len( data_window_matrix_x_values ) ):

		                        line_of_info.append( str(data_window_matrix_x_values[j][i]) )


	                        f.write( ",".join( line_of_info ) )

	                        f.write("\n")
				
				
				



	
	
		
		

#1 allows for single or multiple runs

def single_run(matrix_file_names_list, event_name_arr, max_counter,path_to_data):

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
	
	
	column_labels = "Event Name," + ",".join(matrix_file_names_list)	
		
	global_aggr_csv_file_name = "global_aggr_csv_file.csv"

	create_global_aggr_csv( global_aggr_csv_file_name, column_labels )
		

# how many loops it will take to get through all possible data given that data will be split up into divisions of max_counter

	num_loops_needed = math.ceil( len(event_name_arr) / max_counter )        # take all possible y values and divide them into groups of max_counter.
	
	event_name_string =""	

	start = 0
	end = 0 
	
	
	for total_groups_created in range(1, (num_loops_needed + 1) ): 
	
		data_window_matrix_x_values = []
		
		dir_name = "group_" + str(total_groups_created)
		
		subprocess.run( ["sudo mkdir " + dir_name ], shell = True)
		
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

			#Run commands that are needed for executable
			
			#subprocess.run( ["make clean"], shell = True)
			
			#subprocess.run( ["make openmp"],shell = True)

			csv_file_name = matrix + "_" + "g"+ str(total_groups_created) + ".csv"

            # need to finish typing the line I have below
			subprocess.run( ["sudo perf stat -x , -o " + csv_file_name + " -e " + event_name_string + " ./crs_matmult --matrix "+ matrix + "--output matrix_output_run_"+  ], shell = True) #crs_matmult_omp

			# just created csv file for this run containing results of running perf on this matrix with the given event name string, now want to parse this data and store it a in a list

			single_matrix_x_vals = parse_csv_get_x_vals( csv_file_name )

			data_window_matrix_x_values.append( single_matrix_x_vals )

			subprocess.run( ["sudo mv -f " + csv_file_name + " " + dir_name ] , shell = True)
			
			
			
		

		plot_info_string = "_group_" + str(total_groups_created) + ".png"
			
		#plot_data( matrix_file_names_list, data_window_event_name_arr_subset, data_window_matrix_x_values , plot_info_string)
		
		
		local_aggr_csv_file_name = "group_" + str(total_groups_created) + "_aggr_csv_file.csv"
		
		local_aggr_csv( local_aggr_csv_file_name, column_labels, data_window_event_name_arr_subset, data_window_matrix_x_values )	
		
	
		add_to_global_aggr_csv( global_aggr_csv_file_name, data_window_event_name_arr_subset, data_window_matrix_x_values )
		
		
		subprocess.run( ["sudo mv -f " + local_aggr_csv_file_name + " " + dir_name], shell = True ) 
	
		subprocess.run( ["sudo mv -f " +  "$(ls | grep .png) " + dir_name], shell = True)  

		subprocess.run( ["sudo mv -f "+ dir_name + " " + path_to_data ] , shell = True) 
		
		print("path to data: ", path_to_data)
		print()

		event_name_string =""

		start = end

		
		
	subprocess.run( ["sudo mv -f " + global_aggr_csv_file_name + " " + path_to_data], shell = True ) 
		
			
	for remove_matrix_from_exe_dir in matrix_file_names_list:	
		try:
			os.remove( remove_matrix_from_exe_dir )
			print( remove_matrix_from_exe_dir , " removed successfully")

		except OSError as error:
		
			print(error)
			print("file path can not be removed")





def multi_run(matrix_file_names_list, event_name_arr, max_counter, num_runs, path_to_data):

	
	
	print("path to data: ", path_to_data)
	print()
	
	os.chdir(path_to_data)
	original_working_directory = os.getcwd()
	
	for run_number in range(num_runs):
	
		trial_name = "run_" + str(run_number)
		
		subprocess.run( ["sudo mkdir " + trial_name] , shell = True)
		
		path_to_data = os.path.join(path_to_data, trial_name)	
		
		print("path to data: ", path_to_data)
		print()
		
		single_run(matrix_file_names_list, event_name_arr, max_counter,path_to_data)
		
		#path_to_data = os.chdir("..")
		
		os.chdir(original_working_directory)
		path_to_data = os.getcwd()
		
		print("path to data: ", path_to_data)
		print()
		
		
		
	
	
	
	
	
	
def create_data_directories(path_to_data, trial_name):

	original_working_directory = os.getcwd()
	
	os.chdir(path_to_data)
	
	subprocess.run( ["sudo mkdir " + trial_name], shell = True )
	
	#subprocess.run( ["cd -P"+ trial_name], shell = True )
	
	os.chdir(trial_name)
	
	subprocess.run( ["sudo mkdir " + "multi_run "], shell = True )
	
	os.chdir("multi_run")
	
	subprocess.run( ["sudo mkdir csv_files"], shell = True)
	
	#os.chdir("..")
	
	#os.chdir("multi_run")
	
	#subprocess.run( ["sudo mkdir csv_files"], shell = True)
	
	#os.chdir("..")
	
	os.chdir(original_working_directory)
	
	
	

	
	
########################################################################################################################################################### Main








max_counter = 4

num_runs = 2

run_type = "multi_run"


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

    create_data_directories(path_to_data, trial_name)


    path_to_data = os.path.join(project_home,"data",matrix_name, trial_name, run_type, "csv_files")




    multi_run(matrix_file_names_list, event_name_arr, max_counter, num_runs, path_to_data)












