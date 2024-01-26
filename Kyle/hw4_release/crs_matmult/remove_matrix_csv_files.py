
"""
I copy the matricies into the exe directory. In our case crs_matmult. Then I generate the csv files in this directory, as well as the images. 
After all of this data is generated, I store it in approprate subdirectories based on group name. I then move all of this data to the approprate place in the data directory for our project. 
Because I generate all of the data in this exe directory, I used this program during testing to remove all of this data that was created between testing runs. 



"""

import os
import subprocess

path = os.getcwd()
file_list = os.listdir(path)
for file in file_list:

	if file[0].isdigit():
		new_path = os.path.join(path,file)
		os.remove(new_path)

	if file[0].startswith('g'):
	
		subprocess.run( ["sudo rm -rf "+ file] , shell = True)
		
	if ".png" in file: 
	
		subprocess.run( ["sudo rm -rf "+ file] , shell = True)
		

