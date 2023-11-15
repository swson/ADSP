
import os


# want to pass these values in through a list coming from the main python program controlling all of the other python programs

matrix_name = "494_bus"

file_type = "crs"

file_composition = "non_zero"


path_to_corrupted_files = "../matrix_directory/" + matrix_name + "/" + file_type + "/" + file_composition		# This path relies on the current directory structure

files = os.listdir(path_to_corrupted_files)

#files = ",".join(files) 

path_to_baseline_file = "../matrix_directory/" + matrix_name + "/" + file_type + "/baseline_matrix_uncorrupted"

baseline_file = os.listdir(path_to_baseline_file)



temp = []

temp.append(baseline_file)
temp.append(files)

print(temp)
