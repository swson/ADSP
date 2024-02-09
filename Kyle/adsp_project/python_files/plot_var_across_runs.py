# This program assumes that all of the directory structure from python_controller.py has been established and that python_controller.py has been run already

import os
import csv 
import subprocess
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd




def create_data_structure(num_lists):

	temp = []
	
	empty_list_of_lists = []
	
	for i in range(num_lists):
	
		empty_list_of_lists.append(temp)
		
	return empty_list_of_lists
		



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
	
		line_reader = csv.reader(f)
		
		for row in line_reader:
		
			run_data.append(row)
			
	os.chdir("..")
	
	all_global_aggr_file_data.append(run_data)
	
		
#data structure created, now it is time to parse it	









def empty_list_of_lists():

	list_of_lists = []
	empty_list = []

	for i in range( len( all_global_aggr_file_data[0][0] ) ):

		list_of_lists.append(empty_list)

	return list_of_lists
	

for run in  all_global_aggr_file_data:
	list_of_lists = empty_list_of_lists()
	
	for row in run: 
		
	
		for j in range( len(row) ): 
		
			list_of_lists[j].append(row[j])
		
			
			
		print(list_of_lists)
		print()
	
	print()
	print()
		
			
		
			
	
	
	
		
	
	
	
	
	
	
	


	
	
		

	


	
		




























































	
			

	
