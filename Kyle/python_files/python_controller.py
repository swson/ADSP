import os
import json
import csv
import subprocess
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# want to pass these values in through a list coming from the main python program controlling all of the other python programs

matrix_name = "494_bus"
file_type = "crs"
file_composition = "non_zero"
trial_name = "trial_1"
run_name = "single_run"

microarch_directory_name = "skylake"  # will become list of microarch 
event_file = "pipeline.json"

""""
cache.json" 

"floating-point.json"

"memory.json"

"""


custom_path = "/home/kchai/Documents/current/current_research/professor_Son_research/code/project_demo"	# REPLACE THIS WITH FILE PATH TO PROJECT IN YOUR SYSTEM

project_dir_name = "project_dir_template_demo"			

project_home = os.path.join(custom_path,project_dir_name)		# will travel to all directories relative to project home directory





#Global above, local below if I am making everything below this a file that gets called generically with global inputs from above as parameters





############################################ additional file paths that are subject to project directory structure

path_to_json_file = os.path.join(project_home,"x86",microarch_directory_name, event_file)

path_to_baseline_file = os.path.join(project_home, "matrix_directory",matrix_name,file_type,"baseline_matrix_uncorrupted")
path_to_corrupted_files = os.path.join(project_home,"matrix_directory",matrix_name,file_type,file_composition )

path_to_exe = os.path.join(project_home,"hw4_release","crs_matmult")

path_to_data = os.path.join(project_home,"data",matrix_name,trial_name,run_name,"csv_files")

############################################ Function declarations



def reverse_array_for_graphing(arr):

	new_arr = arr[::-1]
	
	return new_arr
	
	

def round_up(val):

	if ( isinstance(val,float ) ):
		return ( int(val) +1 )
	else:
		return val
		
		

def get_event_names():

	event_name_arr = []
	

	with open(path_to_json_file) as f:              # absolute path to json file
        	contents = json.load(f)

	for c in contents:                      # data in json file is a list of dictionaries
	
		event_name_arr.append( c["EventName"] ) # will be used for graphing later on

	return event_name_arr




def get_matrix_file_names():

	matrix_file_names_list = os.listdir(path_to_baseline_file) + os.listdir(path_to_corrupted_files)	# Joining the two lists together. BASELINE SHOULD ALWAYS BE FIRST ELEMENT
	
	return matrix_file_names_list 	# will be file_name.extension, where extension != csv. ex) if using crs files, all files end in .crs in this list




def run_matmult_process_perf_stat(matrix_file_names_list, event_name_string):

	for i in range( len(matrix_file_names_list) ):
	
		print()
		print(matrix_file_names_list[i])
		print()
	
		if ( i == 0):	
									# dealing with baseline matrix
			os.chdir(path_to_baseline_file)
			
		else: 							# dealing with any other matrix in that list, i.e. corrupted matrix
			os.chdir(path_to_corrupted_files)
			

		subprocess.run( ["cp " + matrix_file_names_list[i] + " " + path_to_exe], shell = True )	
		
		os.chdir(path_to_exe)
		
		print()
		print("chnaging path to : " + path_to_exe)
		print()
		

		#Run commands that are needed for executable
		
		subprocess.run( ["make clean"], shell = True)

		subprocess.run( ["make openmp"],shell = True)
		
	
		subprocess.run( ["sudo perf stat -x , -o " + matrix_file_names_list[i] + ".csv" + " -e " + event_name_string + " ./crs_matmult_omp --matrix "+ matrix_file_names_list[i]], shell = True) 
		
		# move the csv file generated into csv files directory 
		
		subprocess.run( ["mv -f "+ matrix_file_names_list[i] + ".csv" + " " + path_to_data ] , shell = True)
		
		# remove copy of the matrix in exe directory once you are done using it.
		
		try:
			os.remove(matrix_file_names_list[i])
			print(matrix_file_names_list[i] + " removed successfully")

		except OSError as error:
			print(error)
			print("file path can not be removed")
	





def get_data_to_plot():		# this will create the data structure that I will use to plot the graph

	os.chdir(path_to_data)
	
	data = []
	
	file_name_labels_list = []
	
	for csv_file in os.listdir(path_to_data):
	
		print()
		print(csv_file)
		print()
		
		file_name_labels_list.append(csv_file)

		with open(csv_file) as f:
	
			x_values = []
	
			line_reader = csv.reader(f)
	
			for row in line_reader:		# Each row is a list of string values
	
				if len(row) == 0:		# if the list is empty
					continue 
		
				elif row[0].startswith('#'):
					continue
			
		
				elif row[0].startswith('<'):
		 			x_values.append(0)
		 			
				else:
					x_values.append( int( row[0] ) )	# matrix data stored in a list
	

		data.append(x_values)
		
	return data,file_name_labels_list
	
	




def plot_data(data,file_name_labels_list,division_size,event_name_arr):

	temp_x_values = []
	temp_y_values = []
	#temp_file_name_labels_list = []			# how many y values have we gone through as part of our division as well 
	
	graph_dict = {}

	division = round_up( len(event_name_arr) / division_size )
	
	start = 0
	end = division

	# for now, try to plot first 10 values of each file
	
	for i in range ( len(data) ):		# looping through list of matrix data, not matricies themselves. Data should be the same as file_name_labels_list
	
		for j in range(start,end):			#event_name_arr = list of all y values for this graph ....len(event_name_arr)
		
			temp_x_values.append(data[i][j])
			
			if( i == 0):
				temp_y_values.append(event_name_arr[j])	
			
			else:
				continue
			
	
		graph_dict[  file_name_labels_list[i]   ] = temp_x_values	#reverse_array_for_graphing( temp_x_values )
		
		temp_x_values = []
	
	
	
	
	#plt.figure()
	
	df =  pd.DataFrame( graph_dict, index =  temp_y_values )	#reverse_array_for_graphing ( temp_y_values ) )
	
	ax = df.plot.barh()
	plt.xscale('log')
	plt.subplots_adjust(left=.3, right=.9, top=.9, bottom=0.01)
	plt.yticks(fontsize=10)

	plt.show()
		
	temp_y_values = []
	graph_dict = {}
	
	#print(graph_dict)
	
	
	
	
	
	
	
"""	
		temp_data.append( data[i] )
		temp_index.append( temp[i] ) 	
	
		if ( i % division == 0 ):
		
"""			
	


############# main

event_name_string =""	

event_name_string = ",".join( get_event_names() )	

temp = get_event_names()

a = get_matrix_file_names()
 
run_matmult_process_perf_stat(a, event_name_string)

data,file_name_labels_list=get_data_to_plot()

plot_data(data,file_name_labels_list,10,temp)

# now I want to plot this data











		
