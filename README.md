# ADSP
This script takes in files with floating point data and creates a copy with errors injected into them.  
This script can specify the files to inject errors to, magnitude and frequency of the error, three different error metrics, and plot the comparison graph between original and error-injected data. This script also supports comparisons for data characteristics based on DCT (discrete consine transform) coefficients.

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

## File
Input files by default are all files inside a folder named "data", set by global variable INPUT_DIR
````python
INPUT_DIR = "data"
````
Default path can be changed by changing the variable.  
User can also manually input the path to the files. Inputting files that do not meet the file requirements (incorrect file types) will be ignored.  
.bin files and .dat files are read as 64 bit floating point numbers by default, but can be set to 32 bit (refers to optional argument section).  
.nc files require a variable name since .nc files can have multiple sets of data with different variables.  

Output files by default are output to a folder named "result", set by global variable OUTPUT_DIR
````python
OUTPUT_DIR = "result"
````
Default path can be changed by changing the variable.  
Output file names follow the following naming convention:  
`<input file name>_<error metric>_<error rate>_<anomaly rate>.<file type>`

A separate log file containing the metadata for the injection called 'log.txt' will also be created in the current directory. 

#Customization
##Mandatory arguments
###Error rate
-e, --error_rate  
Value of the error, error rate and error metric determine the error bound for the random error injection. 
###Anomaly rate
-a, --anomaly_rate  
Frequency of the error injection, a number between 0 and 1. Number of errors is the product of anomaly type and total number of data points.
###Error metric  
-m, --error_metric  
Error metric controls what kind of error bound, the range for the random error value. There are three types of error injection:
- absolute - error bound is the value of the error rate
- relative - error bound is the difference between max and min of the entire data set multiplied by error rate
- point - error bound is the value of the data being injected multiplied by the error rate
##Optional arguments
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


