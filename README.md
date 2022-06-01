# ADSP
This script takes in files with floating point data and creates file copies with errors injected into them.  
This script can specify the files to inject errors to, magnitude and frequency of the error, using four different error metrics, and plot the comparison graph between original and error-injected data. This script also supports comparisons for data characteristics based on DCT (discrete consine transform) coefficients.

# Requirements
## Software
Python

## Supported File Types
- .csv (Comma Separated Values)  
- .bin (BINary)  
- .dat (DATa)  
- .nc (Network Common data form)  

## Supported Data Types
Little-endian floating point numbers  
Binary files can accept 64-bit and 32-bit data  
NetCDF4 Classic and NetCDF4 are tested to work, other netCDF files should also work but are not tested


## File
### Input files
Input files by default are all files inside a folder named "data", set by global variable INPUT_DIR
````python
INPUT_DIR = "data"
````
Default path can be changed by changing the variable INPUT_DIR, 
user can also manually input the path to the files (refers to optional argument section, --file).  
Inputting files that do not meet the file requirements (incorrect file types) will be ignored and a warning message will be created in the log file.  
.bin files and .dat files are read as 64 bit floating point numbers by default, but can be set to 32 bit (refers to optional argument section, --data_type).  
.nc files require a variable name since .nc files can have multiple sets of data with different variables, if there are nc files are included as input files and there is not a variable, a warning message will be created in the log file (refers to optional argument section, --variable).  

### Output files
Output files by default are output to a folder named "result", set by global variable OUTPUT_DIR
````python
OUTPUT_DIR = "result"
````
Default path can be changed by changing the variable, 
user can also manually input the path to the files (refers to optional argument section, --output)   
Output file names follow the following naming convention:  
`<input file name>_<error metric>_<error rate>_<anomaly rate>.<file type>`

A separate log file containing the metadata for the injection called 'log.txt' will also be created in the current directory, this log file will always output to current directory  

#Customization
##Mandatory arguments
###Error rate
-e, --error_rate  
List of value of the error, error rate and error metric determine the error bound for the random error injection. 
###Anomaly rate
-i, --injection_rate  
List of frequency of the error injection, a number between 0 and 1. Number of errors is the product of anomaly type and total number of data points.
###Error metric  
-m, --error_metric  
List of error metric, controls what kind of error bound is used, the range for the random 
error value. There are five types of error injection:
- absolute_uni - error bound is the value of the error rate, uniform random number generation is used
- relative_uni - error bound is the difference between max and min of the entire data set multiplied by error rate, uniform random number generation is used
- point_uni - error bound is the value of the data being injected multiplied by the error rate, uniform random number generation is used
- absolute_gauss - error generated using gaussian distribution with the original data point being 0 and error_rate being the standard deviation
- point_gauss - error generated using gaussian distribution with the original data point being the mean and error_rate being the standard deviation

##Optional arguments

###Input file
-f, --file  
Notify the script to use the list of file(s) given by the user as the input file(s).  
If this option is not selected the files in default input folder will be used as the input files. 

###Output file
-o, --output  
Notify the script to use the folder given by the user to output the error injected files.  
If this option is not selected the files in default output folder will be used to output files. 

###Data type
-d, --data_type  
This option is used for .bin files only.  
User can specify two options for this argument, 'f' for double precision format and 's' for single precision format. 
By default, all .bin files are treated as 64-bit numbers ('f' is selected), but using this option ('s' is selected) the script will interpret .bin files as 32-bit number format.  

###Variable
-v, --variable  
This option is used for .nc files only.  
This option is required for .nc files, otherwise the script will not know which variable to inject errors on and will output an error message in the log file. User has to put the variable that needs to be injected after this argument to inject the error to the file.

###Plot
-p, --plot  
If true plot the errors one by one, error will be plotted alongside the original data, window size of the plot is set by a global variable PLOT_WINDOW_SIZE defaulted to 100
```python
PLOT_WINDOW_SIZE = 100
```
Default window size can be changed by changing the variable.  
Title of the plot is the name of the original file followed by the order of error.  
###DCT
--dct  
If true computes the DCT of the original data and error data and compares them. Result will be printed on the log file.

###Type of anomaly
-t, --anomaly_type  
Determine if point anomaly or collective anomaly will be injected, this feature is incomplete, currently all anomaly is point injection.

