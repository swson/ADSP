import os
import subprocess


matrix_name = "494_bus"

path_to_converted_mtx_fiiles=os.path.join("../matmult-progs/crs_matmult/matrix_data_crs_format")

exe_list = ["mtx2crs.py","multiple_mtx2crs.py"]


#subprocess.run( ["sudo chmod +x " + exe_name], shell = True)		# want to make program executable in its new context

#subprocess.run( ["sudo chmod +x " + exe_name_2], shell = True)		# want to make program executable in its new context



for matrix in sorted( os.listdir( os.getcwd() ) ):
	
	if (matrix not in exe_list) :
		subprocess.run( [ "sudo ./mtx2crs.py < " + matrix + " > " + path_to_converted_mtx_fiiles + "/" + matrix + ".crs"], shell = True )

