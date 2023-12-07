import os
import subprocess


matrix_name = "1138_bus"
file_type_original = "mtx"
file_type_converted = "crs"
file_composition = "non_zero"




custom_path = "/home/kchai/Documents/current/current_research/professor_Son_research/code/project_demo"	# REPLACE THIS WITH FILE PATH TO PROJECT IN YOUR SYSTEM

project_dir_name = "project_dir_template_demo"			

project_home = os.path.join(custom_path,project_dir_name)		# will travel to all directories relative to project home directory



path_to_downloaded_mtx_files  = os.path.join(project_home,"matrix_directory",matrix_name,file_type_original,file_composition )

path_to_converted_files = os.path.join(project_home,"matrix_directory",matrix_name,file_type_converted,file_composition )


path_to_exe = os.path.join(project_home,"hw4_release","mtx2crs")
exe_name = "mtx2crs.py"


# move conversion program to mtx files directory

os.chdir(project_home)	# this file starts out in the python files directory. need to go to proj home first to get proper scope for directory navigation

os.chdir(path_to_exe)

subprocess.run( ["cp " + exe_name + " " + path_to_downloaded_mtx_files], shell = True )

os.chdir(path_to_downloaded_mtx_files)

subprocess.run( ["sudo chmod +x " + exe_name], shell = True)		# want to make program executable in its new context



print(os.listdir(path_to_downloaded_mtx_files) )

	

print()

for matrix in os.listdir(path_to_downloaded_mtx_files):
	
	if matrix != exe_name:
	
		subprocess.run( [ "sudo ./mtx2crs.py < " + matrix + " > " + path_to_converted_files + "/" + matrix + ".crs"], shell = True )
		
		
		#./mtx2crs.py < ../mat/mat_494/494_bus/494_bus.mtx > ../mat_cache/crs/494_bus.crs
		
		
subprocess.run( ["rm " + exe_name ], shell = True )

print(os.listdir(path_to_downloaded_mtx_files) )		










		
	

