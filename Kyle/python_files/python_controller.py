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

project_home = os.getcwd()  #Changing path from python_files folder to project home directory


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
		
		
		
		
		
		
def local_aggr_csv( aggr_csv_file_name, column_labels, data_window_event_name_arr_subset, data_window_matrix_x_values):

#data_window_event_name_arr_subset, data_window_matrix_x_values, aggr_csv_file_name, column_labels):

	with open(aggr_csv_file_name,"a+") as f:
	
		
		f.write( column_labels + "\n" ) 

		for i in range( len(data_window_event_name_arr_subset) ):
	
			line_of_info = []

			line_of_info.append( data_window_event_name_arr_subset[i] )


			for j in range( len( data_window_matrix_x_values ) ):

				line_of_info.append( str(data_window_matrix_x_values[j][i]) )


			f.write( ",".join( line_of_info ) )

			f.write("\n")
				


				
				
def create_global_aggr_csv(aggr_csv_file_name,column_labels):

	f =  open(aggr_csv_file_name,"w+")
	
	f.write( column_labels + "\n" ) 
	
	f.close()
					


				
				

def add_to_global_aggr_csv( aggr_csv_file_name, data_window_event_name_arr_subset, data_window_matrix_x_values):

	with open(aggr_csv_file_name,"a+") as f:
	
		
		for i in range( len(data_window_event_name_arr_subset) ):

			line_of_info = []

			line_of_info.append( data_window_event_name_arr_subset[i] )


			for j in range( len( data_window_matrix_x_values ) ):

				line_of_info.append( str(data_window_matrix_x_values[j][i]) )


			f.write( ",".join( line_of_info ) )

			f.write("\n")
				
				
				



	
	
		
		


def single_run(matrix_file_names_list, event_name_arr, max_counter):

	print("matrix_file_names_list: ", matrix_file_names_list)
	print()
	print()
	

	
	for i  in range( len(matrix_file_names_list) ):		               # go through all of the matrix files being used one by one


		if ( i == 0 ):

			os.chdir(path_to_baseline_file)
			
			print("current path: " + path_to_baseline_file)
			print()

			subprocess.run( ["cp " + matrix_file_names_list[i] + " " + path_to_exe], shell = True )	    # copy matrix being tested into exe directory

			
        
		else:
			os.chdir(path_to_corrupted_files)
			print("current path: " + path_to_corrupted_files)
			print()
			
			subprocess.run( ["cp " + matrix_file_names_list[i] + " " + path_to_exe], shell = True )	    # copy matrix being tested into exe directory
		


	os.chdir(path_to_exe)		# Changing from the python files directory this program was ran from into the directory where the execuatble is
	
	
	column_labels = "Event Name " + ",".join(matrix_file_names_list)	
		
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
			
			subprocess.run( ["make clean"], shell = True)
			
			subprocess.run( ["make openmp"],shell = True)

			csv_file_name = matrix + "_" + "g"+ str(total_groups_created) + ".csv"

			subprocess.run( ["sudo perf stat -x , -o " + csv_file_name + " -e " + event_name_string + " ./crs_matmult_omp --matrix "+ matrix], shell = True) #crs_matmult_omp

			# just created csv file for this run containing results of running perf on this matrix with the given event name string, now want to parse this data and store it a in a list

			single_matrix_x_vals = parse_csv_get_x_vals( csv_file_name )

			data_window_matrix_x_values.append( single_matrix_x_vals )

			subprocess.run( ["sudo mv -f " + csv_file_name + " " + dir_name ] , shell = True)
			
			
			
		

		plot_info_string = "_group_" + str(total_groups_created) + ".png"
			
		plot_data( matrix_file_names_list, data_window_event_name_arr_subset, data_window_matrix_x_values , plot_info_string)
		
		
		local_aggr_csv_file_name = "group_" + str(total_groups_created) + "_aggr_csv_file.csv"
		
		local_aggr_csv( local_aggr_csv_file_name, column_labels, data_window_event_name_arr_subset, data_window_matrix_x_values )	
		
	
		add_to_global_aggr_csv( global_aggr_csv_file_name, data_window_event_name_arr_subset, data_window_matrix_x_values )
		
		
		subprocess.run( ["sudo mv -f " + local_aggr_csv_file_name + " " + dir_name], shell = True ) 
	
		subprocess.run( ["sudo mv -f " +  "$(ls | grep .png) " + dir_name], shell = True)  

		subprocess.run( ["sudo mv -f "+ dir_name + " " + path_to_data ] , shell = True) 
		

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

	
	
	
	
######################################################## Main


event_name_arr = get_event_names()

event_name_arr = event_name_arr[:8]	# just doing this for testing purposes. Remove later

matrix_file_names_list = get_matrix_file_names()

max_counter = 8

single_run(matrix_file_names_list, event_name_arr, max_counter)















