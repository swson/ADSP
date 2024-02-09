import os
import subprocess


matrix_name = "494_bus"
file_type_original = "mtx"
file_type_converted = "crs"
file_composition = "non_zero"


os.chdir("..")
project_home = os.getcwd()






path_to_downloaded_mtx_files  = os.path.join(project_home,"matrix_directory",matrix_name,file_type_original,file_composition )

path_to_converted_files = os.path.join(project_home,"matrix_directory",matrix_name,file_type_converted,file_composition )


path_to_exe = os.path.join(project_home,"python_files")
exe_name = "multiple_mtx2crs.py"
exe_name_2 = "mtx2crs.py"
os.chdir(path_to_exe)



subprocess.run( ["cp " + exe_name + " " + path_to_downloaded_mtx_files], shell = True )

subprocess.run( ["cp " + exe_name_2 + " " + path_to_downloaded_mtx_files], shell = True )

os.chdir(path_to_downloaded_mtx_files)


subprocess.run( ["sudo chmod +x " + exe_name], shell = True)		# want to make program executable in its new context

subprocess.run( ["sudo chmod +x " + exe_name_2], shell = True)		# want to make program executable in its new context


print(os.listdir(path_to_downloaded_mtx_files) )
print()

for matrix in sorted(  os.listdir(path_to_downloaded_mtx_files) ):
	
	if (matrix != exe_name) and (matrix != exe_name_2):
	
		subprocess.run( [ "sudo ./mtx2crs.py < " + matrix + " > " + path_to_converted_files + "/" + matrix + ".crs"], shell = True )
		
		
		#./mtx2crs.py < ../mat/mat_494/494_bus/494_bus.mtx > ../mat_cache/crs/494_bus.crs
		
		
subprocess.run( ["rm " + exe_name ], shell = True )


subprocess.run( ["rm " + exe_name_2 ], shell = True )

print(sorted(os.listdir(path_to_downloaded_mtx_files) ))		










		
	

