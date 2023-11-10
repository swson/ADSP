
import matplotlib.pyplot as plt
import numpy as np

import pandas as pd 

import csv




def make_arrays_same_lenght(array_1,array_2):



	if (len(array_1) > len(array_2)):
	
		while (len(array_1) > len(array_2)):
			
			array_2.append(0)
			
		return array_1,array_2
		
			
	elif (len(array_2) > len(array_1)):
	
		while (len(array_2) > len(array_1)):
			
			array_1.append(0)
			
		return array_1,array_2
		
	else: 
	
		return array_1,array_2
			
	





x_values=[]

y_values=[]


x_values_corrupted = []

y_values_corrupted = []


value_string =""

file_to_graph = "/home/kchai/Documents/current/current_research/professor_Son_research/hw4_release/crs_matmult/temp_shell_output_baseline.csv"

file_to_graph_corrupted = "/home/kchai/Documents/current/current_research/professor_Son_research/hw4_release/crs_matmult/temp_shell_output_corrupted.csv"


with open(file_to_graph) as f:

	line_reader = csv.reader(f)
	
	for row in line_reader:		# Each row is a list of string values
	
		if len(row) == 0:		# if the list is empty
			continue 
		
		elif row[0].startswith('#') or row[0].startswith('<'):
			continue
		else:
		
			x_values.append( int( row[0] ) )
			
			y_values.append(row[2])
			
	



with open(file_to_graph_corrupted) as f:

	line_reader = csv.reader(f)
	
	for row in line_reader:		# Each row is a list of string values
	
		if len(row) == 0:		# if the list is empty
			continue 
		
		elif row[0].startswith('#') or row[0].startswith('<'):
			continue
		else:
		
			x_values_corrupted.append( int( row[0] ) )
			
			y_values_corrupted.append(row[2])





x_values,x_values_corrupted = make_arrays_same_lenght(x_values,x_values_corrupted)



original = x_values
corrupted = x_values_corrupted

if (len(y_values_corrupted) > len(y_values)):

	index = y_values_corrupted
else:

	index = y_values
	
	


df = pd.DataFrame({'original': original,'corrupted': corrupted}, index=index)

ax = df.plot.barh()
plt.xscale('log')

plt.suptitle("Skylake pipeline-branch events")
plt.title("Baseline matmult.c 494_bus compared to 494_bus_gauss_0p10_0p10_sym_nonzero.crs ")

"""

for i,value in enumerate(x_values):

	ax.text(value + ,,str(value))
	
for i,value in enumerate(x_values_corrupted):

	ax.text(value,i,str(value))
	
"""

plt.show()



#x value arrays should be the same based on function

#need to make function to use greater of the 2 y values as the labels for the graph




for i in range(len(index)-1):

	print(index[i] + "				" + str(x_values[i])+ "					" + str(x_values_corrupted[i]))
	



















