import os
import json
import csv 
import subprocess
import time
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
import math

matrix_name = "494_bus"
file_type = "crs"
file_composition = "non_zero"
trial_name = "trial_1"
run_name = "single_run"

microarch_directory_name = "skylake"  # will become list of microarch 

event_file_list = ["pipeline.json", "cache.json" , "floating-point.json","memory.json"] 

event_file = event_file_list[0]




os.chdir("..")

project_home = os.getcwd()


############################################ additional file paths that are subject to project directory structure

path_to_json_file = os.path.join(project_home,"x86",microarch_directory_name, event_file)

path_to_baseline_file = os.path.join(project_home, "matrix_directory",matrix_name,file_type,"baseline_matrix_uncorrupted")
path_to_corrupted_files = os.path.join(project_home,"matrix_directory",matrix_name,file_type,file_composition )

path_to_exe = os.path.join(project_home,"hw4_release","crs_matmult")

path_to_data = os.path.join(project_home,"data",matrix_name,trial_name,run_name,"csv_files")

############################################ Function declarations


def get_event_names():

    event_name_arr = []


    with open(path_to_json_file) as f:              # absolute path to json file
            contents = json.load(f)

    for c in contents:                      # data in json file is a list of dictionaries

        event_name_arr.append( c["EventName"] ) # will be used for graphing later on

    return event_name_arr





def get_matrix_file_names():

    matrix_file_names_list = os.listdir(path_to_baseline_file) + os.listdir(path_to_corrupted_files)    # Joining the two lists together. BASELINE SHOULD ALWAYS BE FIRST ELEMENT

    return matrix_file_names_list   # will be file_name.extension, where extension != csv. ex) if using crs files, all files end in .crs in this list




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
				matrix_x_vals.append( int( row[0] ) )	# matrix data stored in a list
	

	return matrix_x_vals




def plot_data( matrix_file_names_list, data_window_event_name_arr_subset, data_window_matrix_x_values, plot_info_string ):

		temp_y_values = data_window_event_name_arr_subset
		
		graph_dict = {}
	
	
		print( "len(matrix_file_names_list) ", len(matrix_file_names_list) )
		print()
		print( "len(data_window_matrix_x_values) ", len(data_window_matrix_x_values) )
		print()
	
		for i in range( len(matrix_file_names_list) -1 ):
		
			graph_dict[ matrix_file_names_list[i] ] = data_window_matrix_x_values[i]
			
		

		df =  pd.DataFrame( graph_dict, index =  temp_y_values )	

		ax = df.plot.barh(width = .85)	#width = .7 

		plt.xscale('log')

		plt.subplots_adjust(left=.3, right=.9, top=.9, bottom=0.05)
		
		plt.yticks(fontsize=9)

		

		ax.legend(loc='upper center', bbox_to_anchor=(0.35, 1.1),
		fancybox=True, shadow=True, ncol= len(matrix_file_names_list))

		for container in ax.containers:

			ax.bar_label(container,padding=5)

		plt.title("Event Monitored: " + event_file + " Group: " + plot_info_string)
		
		image_name = event_file + "_group_" + plot_info_string + ".png"
		
		#plt.figure(figsize=(20,20))
		
		#plt.figure()
		#plt.rcParams['figure.figsize'] = [200, 200]
		plt.tight_layout()
		plt.savefig( image_name, dpi = 100 )	#dpi = 200
		
		#plt.show()
		


def testing(matrix_file_names_list, event_name_arr, max_counter):

	"""
	print(event_name_arr)
	print()

	print("len(event_name_arr): ", len(event_name_arr))
	print()
	
	
	
	print("num_loops_needed: ", num_loops_needed)
	print()
	"""
	
	
	
	for i  in range( len(matrix_file_names_list) ):		               # go through all of the matrix files being used one by one


		if ( i == 0):

			print()
			print()
			print("opening baseline file now")                                  # baseline matrix should alyays be first entry in list. 
			print()
			print()

			os.chdir(path_to_baseline_file)

		else: 							# dealing with any other matrix in that list, i.e. corrupted matrix
			os.chdir(path_to_corrupted_files)
	
		
		subprocess.run( ["cp " + matrix_file_names_list[i] + " " + path_to_exe], shell = True )	    # copy matrix being tested into exe directory
		
		
		
		
	os.chdir(path_to_exe)		# Changing from the python files directory this program was ran from into the directory where the execuatble is
		
		
		

# how many loops it will take to get through all possible data given that data will be split up into divisions of max_counter

	num_loops_needed = math.ceil( len(event_name_arr) / max_counter )        # take all possible y values and divide them into groups of max_counter.
	
	event_name_string =""	

	start = 0
	end = 0 
	
	
	for total_groups_created in range(1, (num_loops_needed + 1) ): 
	
		data_window_matrix_x_values = []
		
		dir_name = "group_" + str(total_groups_created)
		
		subprocess.run( ["sudo mkdir " + dir_name ], shell = True)

		#new_path_to_data = os.path.join( path_to_data, dir_name ) 

		if ( total_groups_created * max_counter ) > len(event_name_arr):

			end = end + len(event_name_arr) - start                                  

		else:
			end = ( total_groups_created * max_counter )



		
		for j in range(start,end):            # division data window is the space between these running start and end values


			if j == start:             # creating event name string that will be passed to perf stat command, containing max_counter event_names 

				event_name_string = event_name_string + event_name_arr[j]
				
				#temp_y_values.append( event_name_arr[j] )

			else:

				event_name_string = event_name_string +","+ event_name_arr[j]

				#temp_y_values.append( event_name_arr[j] )
			
	
	
	
		for matrix in ( matrix_file_names_list ):		               # go through all of the matrix files being used one by one
	
		
			print("event_name_string: ", event_name_string)
			print()

			#Run commands that are needed for executable
			
			subprocess.run( ["make clean"], shell = True)
			
			subprocess.run( ["make openmp"],shell = True)
			
			subprocess.run( ["sudo perf stat -x , -o " + matrix + "_" + "g"+ str(total_groups_created) + ".csv" + " -e " + event_name_string + " ./crs_matmult_omp --matrix "+ matrix], shell = True) #crs_matmult_omp
			
	
			# just created csv file for this run, now want to parse it and store data in a list
			
	
			csv_file_name = matrix + "_" + "g"+ str(total_groups_created) + ".csv"
			
			single_matrix_x_vals = parse_csv_get_x_vals( csv_file_name )
	
			data_window_matrix_x_values.append( single_matrix_x_vals )
	
			
			data_window_event_name_arr_subset = event_name_string.split(',')
			

			
			subprocess.run( ["sudo mv -f "+ matrix + "_" + "g"+ str(total_groups_created) + ".csv "  + dir_name ] , shell = True)
			
			
			

		


		plot_info_string = str(total_groups_created)
			
		plot_data( matrix_file_names_list, data_window_event_name_arr_subset, data_window_matrix_x_values , plot_info_string)
		
		subprocess.run( ["sudo mv -f " +  "$(ls | grep .png) " + dir_name], shell = True)  #FIXME I concatonated $... to this line, I think I actually want the double quotes around this. ex "$..." This didn't solve the issue as much. I put the line in the right place, but the line itself isn't completely correct. 


		subprocess.run( ["sudo mv -f "+ dir_name + " " + path_to_data ] , shell = True) 

		event_name_string =""

		start = end

		
			
			
			
			
			
			
	for remove_matrix_from_exe_dir in matrix_file_names_list:
	
	
		try:
			os.remove( remove_matrix_from_exe_dir )
			print( remove_matrix_from_exe_dir , " removed successfully")

		except OSError as error:
		
			print(error)
			print("file path can not be removed")

	
	
	
	
	
	
	
	
	
######################################################## Main


event_name_arr = get_event_names()

#event_name_arr = event_name_arr[:8]	# just doing this for testing purposes. Remove later

matrix_file_names_list = get_matrix_file_names()

max_counter = 8

testing(matrix_file_names_list, event_name_arr, max_counter)















