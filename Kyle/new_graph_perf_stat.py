
import matplotlib.pyplot as plt
import numpy as np

import pandas as pd 

import csv
import math


def reverse_array_for_graphing(arr):

	new_arr = arr[::-1]
	
	return new_arr


"""
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
			
"""

x_values=[]

y_values=[]


x_values_corrupted = []

y_values_corrupted = []


value_string =""

file_to_graph = "/home/kchai/Documents/current/current_research/professor_Son_research/hw4_release/crs_matmult/temp_shell_output_baseline.csv"

file_to_graph_corrupted = "/home/kchai/Documents/current/current_research/professor_Son_research/hw4_release/crs_matmult/temp_shell_output_corrupted.csv"



all_y_axis_values = ['INST_RETIRED.ANY_P', 'UOPS_EXECUTED.STALL_CYCLES', 'EXE_ACTIVITY.4_PORTS_UTIL', 'ARITH.DIVIDER_ACTIVE', 'LD_BLOCKS_PARTIAL.ADDRESS_ALIAS', 'BR_INST_RETIRED.FAR_BRANCH', 'UOPS_EXECUTED.X87', 'LOAD_HIT_PRE.SW_PF', 'BR_MISP_RETIRED.NEAR_CALL', 'CYCLE_ACTIVITY.STALLS_TOTAL', 'UOPS_ISSUED.SLOW_LEA', 'UOPS_RETIRED.TOTAL_CYCLES', 'CPU_CLK_UNHALTED.THREAD_P', 'UOPS_EXECUTED.CYCLES_GE_2_UOPS_EXEC', 'CPU_CLK_THREAD_UNHALTED.REF_XCLK', 'MACHINE_CLEARS.COUNT', 'CPU_CLK_UNHALTED.THREAD_ANY', 'UOPS_EXECUTED.THREAD', 'UOPS_EXECUTED.CYCLES_GE_3_UOPS_EXEC', 'UOPS_EXECUTED.CORE_CYCLES_NONE', 'EXE_ACTIVITY.BOUND_ON_STORES', 'CYCLE_ACTIVITY.CYCLES_L1D_MISS', 'LSD.CYCLES_ACTIVE', 'INT_MISC.RECOVERY_CYCLES', 'CPU_CLK_UNHALTED.REF_XCLK', 'UOPS_DISPATCHED_PORT.PORT_0', 'UOPS_DISPATCHED_PORT.PORT_1', 'UOPS_DISPATCHED_PORT.PORT_2', 'UOPS_DISPATCHED_PORT.PORT_3', 'UOPS_DISPATCHED_PORT.PORT_4', 'UOPS_DISPATCHED_PORT.PORT_5', 'UOPS_DISPATCHED_PORT.PORT_6', 'UOPS_DISPATCHED_PORT.PORT_7', 'INT_MISC.RECOVERY_CYCLES_ANY', 'INST_RETIRED.PREC_DIST', 'LSD.CYCLES_4_UOPS', 'EXE_ACTIVITY.3_PORTS_UTIL', 'LD_BLOCKS.STORE_FORWARD', 'CPU_CLK_THREAD_UNHALTED.REF_XCLK_ANY', 'PARTIAL_RAT_STALLS.SCOREBOARD', 'UOPS_ISSUED.STALL_CYCLES', 'BR_INST_RETIRED.COND_NTAKEN', 'UOPS_EXECUTED.CORE_CYCLES_GE_3', 'UOPS_EXECUTED.CORE_CYCLES_GE_1', 'UOPS_EXECUTED.CORE_CYCLES_GE_4', 'CPU_CLK_UNHALTED.REF_TSC', 'BR_MISP_RETIRED.ALL_BRANCHES', 'OTHER_ASSISTS.ANY', 'UOPS_RETIRED.STALL_CYCLES', 'LSD.UOPS', 'CPU_CLK_THREAD_UNHALTED.ONE_THREAD_ACTIVE', 'ILD_STALL.LCP', 'RS_EVENTS.EMPTY_END', 'CYCLE_ACTIVITY.CYCLES_MEM_ANY', 'BR_INST_RETIRED.NEAR_TAKEN', 'LD_BLOCKS.NO_SR', 'UOPS_ISSUED.ANY', 'CPU_CLK_UNHALTED.THREAD', 'CPU_CLK_UNHALTED.REF_XCLK_ANY', 'BR_INST_RETIRED.NEAR_CALL', 'ROB_MISC_EVENTS.PAUSE_INST', 'RESOURCE_STALLS.ANY', 'MACHINE_CLEARS.SMC', 'CYCLE_ACTIVITY.STALLS_L2_MISS', 'CPU_CLK_UNHALTED.ONE_THREAD_ACTIVE', 'UOPS_EXECUTED.CYCLES_GE_4_UOPS_EXEC', 'BR_MISP_RETIRED.NEAR_TAKEN', 'CYCLE_ACTIVITY.STALLS_MEM_ANY', 'EXE_ACTIVITY.EXE_BOUND_0_PORTS', 'INST_RETIRED.TOTAL_CYCLES_PS', 'UOPS_RETIRED.RETIRE_SLOTS', 'CPU_CLK_UNHALTED.THREAD_P_ANY', 'UOPS_ISSUED.VECTOR_WIDTH_MISMATCH', 'UOPS_RETIRED.MACRO_FUSED', 'ROB_MISC_EVENTS.LBR_INSERTS', 'RS_EVENTS.EMPTY_CYCLES', 'INST_RETIRED.ANY', 'UOPS_EXECUTED.CORE_CYCLES_GE_2', 'RESOURCE_STALLS.SB', 'CPU_CLK_UNHALTED.RING0_TRANS', 'BR_INST_RETIRED.ALL_BRANCHES_PEBS', 'BR_MISP_RETIRED.ALL_BRANCHES_PEBS', 'BR_INST_RETIRED.NEAR_RETURN', 'EXE_ACTIVITY.1_PORTS_UTIL', 'BR_INST_RETIRED.NOT_TAKEN', 'BR_INST_RETIRED.CONDITIONAL', 'BR_MISP_RETIRED.CONDITIONAL', 'UOPS_EXECUTED.CORE', 'CYCLE_ACTIVITY.STALLS_L1D_MISS', 'EXE_ACTIVITY.2_PORTS_UTIL', 'INT_MISC.CLEAR_RESTEER_CYCLES', 'BR_INST_RETIRED.ALL_BRANCHES', 'UOPS_EXECUTED.CYCLES_GE_1_UOP_EXEC', 'CYCLE_ACTIVITY.CYCLES_L2_MISS']


"""
with open(file_to_graph) as f:		# reading baseline file

	line_reader = csv.reader(f)
	
	for row in line_reader:		# Each row is a list of string values
	
		if len(row) == 0:		# if the list is empty
			continue 
		
		elif row[0].startswith('#'):
			continue
		
		elif row[0].startswith('<'):
			x_values.append(0)
		else:
		
			x_values.append( int( row[0] ) )
			
			#y_values.append(row[2])
			
	



with open(file_to_graph_corrupted) as f:	# reading corrupted file

	line_reader = csv.reader(f)
	
	for row in line_reader:		# Each row is a list of string values
	
		if len(row) == 0:		# if the list is empty
			continue 
		
		elif row[0].startswith('#'):
			continue
			
		
		elif row[0].startswith('<'):
		 	x_values_corrupted.append(0)
		else:
		
			x_values_corrupted.append( int( row[0] ) )
			
			#y_values_corrupted.append(row[2])


"""

# at this point I have all of the events that were activated by the baseline program run and all of the events that were activated by the corrupted run

# need to compare these to the overall total amount of y values possible ( all of the event names in the json file) 





#x_values,x_values_corrupted = make_arrays_same_lenght(x_values,x_values_corrupted)


original = reverse_array_for_graphing(x_values)
corrupted = reverse_array_for_graphing(x_values_corrupted)






plt.figure()

index = reverse_array_for_graphing(all_y_axis_values)




	
df = pd.DataFrame({'original': original,'corrupted': corrupted}, index=index)

ax = df.plot.barh()
plt.xscale('log')

plt.suptitle("Skylake pipeline-branch events")
plt.title("Baseline matmult.c 494_bus compared to 494_bus_gauss_0p01_0p01_sym_nonzero.crs ")

plt.subplots_adjust(left=.3, right=.9, top=.9, bottom=0.01)
plt.yticks(fontsize=10)


plt.figure()


plt.show()



#x value arrays should be the same based on function

#need to make function to use greater of the 2 y values as the labels for the graph




















