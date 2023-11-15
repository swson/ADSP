
import os


# want to pass these values in through a list coming from the main python program controlling all of the other python programs

matrix_name = "494_bus"

file_type = "crs"

file_composition = "non_zero"

path_to_files = "../matrix_directory/" + matrix_name + "/" + file_type + "/" + file_composition		# This path relies on the current directory structure

files = os.listdir(path_to_files)

files = ",".join(files) 

print(files)
