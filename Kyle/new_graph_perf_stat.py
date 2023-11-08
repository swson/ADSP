
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







#n = np.arrange(441664, 219296, 11313300, 5503670, 13023188, 837823, 40880, 4220932, 108957, 139700, 85588, 567724, 932818, 2060527, 8257130, 4627980)

#c = np.arrange(735244, 214816, 8244074, 5442930, 10804861, 696188, 11134, 1937030, 82437, 127761, 55588, 326410, 709999, 1848923, 8142112, 797703, 16453, 135505, 148414)

"""

plt.figure()

plt.subplot(211)

plt.barh( y_values,x_values )

#plt.barh(y_values,x_values_corrupted)

plt.xscale('log')

#plt.title("Baseline matmult.c 494_bus compared to 494_bus_gauss_0p01_0p01_sym_nonzero.crs")

plt.title("Baseline matmult.c 494_bus")

plt.tick_params(axis='y', which='major', labelsize=8)

plt.tight_layout()


plt.subplot(212)

plt.barh(y_values_corrupted,x_values_corrupted)

plt.xscale('log')

plt.title("494_bus_gauss_0p01_0p01_sym_nonzero.crs")

plt.tick_params(axis='y', which='major', labelsize=8)

plt.tight_layout()


plt.show()

"""









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
	















#[441664, 219296, 11313300, 5503670, 13023188, 837823, 40880, 4220932, 108957, 139700, 85588, 567724, 932818, 2060527, 8257130, 462798]

#[735244, 214816, 8244074, 5442930, 10804861, 696188, 11134, 1937030, 82437, 127761, 55588, 326410, 709999, 1848923, 8142112, 797703, 16453, 135505, 148414]




"""
print(x_values)
print()
print(x_values_corrupted)



#[441664, 219296, 11313300, 5503670, 13023188, 837823, 40880, 4220932, 108957, 139700, 85588, 567724, 932818, 2060527, 8257130, 462798]




# Numbers of pairs of bars you want
N = 16

# Data on X-axis

# Specify the values of blue bars (height)
blue_bar = x_values
# Specify the values of orange bars (height)
orange_bar = x_values_corrupted

# Position of bars on x-axis
ind = np.arange(N)

# Figure size
plt.figure(figsize=(10,5))

# Width of a bar 
width = 0.3       

# Plotting
plt.barh(ind, blue_bar , width, label='Blue bar label')
plt.barh(ind + width, orange_bar, width, label='Orange bar label')

plt.xlabel('Here goes x-axis label')
plt.ylabel('Here goes y-axis label')
plt.title('Here goes title of the plot')

# xticks()
# First argument - A list of positions at which ticks should be placed
# Second argument -  A list of labels to place at the given locations
#plt.xticks(ind + width / 2, ('Xtick1', 'Xtick3', 'Xtick3'))

# Finding the best position for legends and putting it
plt.legend(loc='best')
plt.show()






df = pd.DataFrame(data={'original': x_values, 'corrupted': x_values_corrupted }, index=2)

ax = df.plot(kind='barh', ylabel='Date', title='My Plot', figsize=(5, 4))

ax.set(xlabel='Value')
for c in ax.containers:
    # set the bar label
    ax.bar_label(c, fmt='%.0f', label_type='edge')
    
ax.margins(x=0.1)

# move the legend out of the plot
ax.legend(title='Columns', bbox_to_anchor=(1, 1.02), loc='upper left')

"""






