# This program assumes that all of the directory structure from python_controller.py has been established and that python_controller.py has been run already
# this program plots the variance across runs normal and corrupted for a given event when for a given matrix being run


import os
import csv 
import subprocess
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd


 



def create_data_structure(dict_key_template):

	new_dict = {}
	
	for k in list (dict_key_template.keys()):
	
		new_dict[k] = []
		
	return new_dict



def create_graph(row_data_across_all_files,path_to_data):

	#dict_val_list =  list( row_data_across_all_files.values() ) 

	#title = row_data_across_all_files[dict_key_list[0]]
	
	#print()
	#print(dict_val_list)


	#event_name_list = row_data_across_all_files.pop(event
	
	original_directory = path_to_data	#path_to_data = os.path.join(project_home,"data",matrix_name,event_name,"multi_run","csv_files")
	
	print(os.getcwd())
	print()
	
	os.chdir("..")
	
	print(os.getcwd())
	print()
	
	subprocess.run( ["sudo mkdir -m a=rwx " + "event_deviation_across_runs" ], shell = True)
	os.chdir("event_deviation_across_runs")
	
	print(os.getcwd())
	print()
	
	all_data = []
	labels = []
	
	for k,v in row_data_across_all_files.items():
	
		labels.append(k)
		all_data.append(v)
		
	labels.pop(0)
	title_temp_var = all_data[0][0] 
	
	subprocess.run( ["sudo mkdir -m a=rwx " + title_temp_var ], shell = True)
	
	os.chdir(title_temp_var)
	print(os.getcwd())
	print()
	
	all_data.pop(0)
	
	for arr in all_data: 			#converting all data in list of lists from strings to ints
		for i in range(len(arr)):
			arr[i] = int(arr[i])
	
	
	print()
	print()
	
	print(labels)
	print()
	
	print(all_data)
	
	
	
	"""
	fig = plt.figure(figsize =(10, 7))

	plt.title("pipeline, " +title_temp_var )
	# Creating plot
	#bplot1 = plt.boxplot(data)
	
	bplot1 = plt.boxplot(all_data,
	vert=True,  # vertical box alignment
	patch_artist=True,  # fill with color
	labels=labels)

	# show plot
	plt.show()
	"""
	
	#fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(9, 4))
	
	fig1 = plt.figure(figsize =(10, 7))
	
	#fig1 = plt.tight_layout()

	# rectangular box plot
	bplot1 = plt.boxplot(all_data[:5],		# this slicing relies on the fact that I am only dealing with 10 files. WILL NEED TO CHANGE THIS IF PROCESSING ANYTHING OTHER THAN 10 FILES
	vert=False,  # vertical box alignment
	patch_artist=True,  # fill with color
	labels=labels[:5])  # will be used to label x-ticks
	plt.title(title_temp_var )
	plt.subplots_adjust(left=.3, right=.9, top=.9, bottom=0.05)
	plt.yticks(fontsize=9)
	image_name = title_temp_var+ "_first_half" + ".png"
	plt.savefig( image_name, bbox_inches = 'tight')

	fig2 = plt.figure(figsize =(10, 7))
	# notch shape box plot
	bplot2 = plt.boxplot(all_data[5:],
	vert=False,  # vertical box alignment
	patch_artist=True,  # fill with color
	labels=labels[5:])  # will be used to label x-ticks
	plt.title(title_temp_var )
	plt.subplots_adjust(left=.3, right=.9, top=.9, bottom=0.05)
	plt.yticks(fontsize=9)
	image_name = title_temp_var+ "_second_half" + ".png"
	plt.savefig( image_name, bbox_inches = 'tight')
	
	#plt.show()
	
	os.chdir(original_directory)
	
	print(os.getcwd())
	print()
	





matrix_name = "494_bus"
event_name = "pipeline.json"


os.chdir("..")
project_home = os.getcwd()  #Changing path from python_files folder to project home directory


path_to_data = os.path.join(project_home,"data",matrix_name,event_name,"multi_run","csv_files")

os.chdir(path_to_data)


all_runs = sorted( os.listdir( path_to_data ) ) 

#creating data structure to hold all global aggr csv file information for each run

all_global_aggr_file_data = []

for run in all_runs: 
	
	os.chdir(run)
	
	with open("global_aggr_csv_file.csv") as f:
	
		run_data = []
	
		line_reader = csv.DictReader(f)
		
		for row in line_reader:
		
			run_data.append(row)
			
	os.chdir("..")
	
	all_global_aggr_file_data.append(run_data)
	
	#print(all_global_aggr_file_data)
	#print()

	
#data structure created, now it is time to parse it	



dict_key_template = all_global_aggr_file_data[0][0]		# all of these dictionary keys from the first row of the first file, are going to be the same across every file
						# using this to create a new dictionary template for run info
						


#print(	row_data_across_all_files )
#print()	




for i in range( len(all_global_aggr_file_data[0])):

	#print(all_global_aggr_file_data[0][i])		# this prints all the rows in the first file
	#print()
	
	row_data_across_all_files = create_data_structure(dict_key_template)

	for file in all_global_aggr_file_data:		# gets the ith row in each file
	
		print(file[i])
		print()
		
		for k,v in file[i].items():
		#print(k,v)
			row_data_across_all_files[k].append(v)
	print()
	print("row_data_across_all_files ", row_data_across_all_files)	# would generate graph with this data now
	create_graph(row_data_across_all_files,path_to_data)
		
	print()
	print()























	
	
		
	
	
	
	
	
	
	


	
	
		

	


	
		




























































	
			

	
