
"""
runs perf list to get a list of all of the hardware event counters available on machine.

Each architecture has a maximum number of counters it can dedicate before it has to share time between all of them. This introduces unwanted overhead.

For our particular machine (intel Skylake) the max number of hardware counters is 4, which is reflected by the global variable max_counter. See perf documentation for your specific system.

for each event available, group them into groups of max_counter. Run perf stat for each counter group with workload being the matrix multiplication program.

  ** can run whatever matrix you want through the matrix multiplication. In this instance, just the uncorrupted matrix was run through it.

combines all results into one aggregate file.

This program also has a function to take the results of each run, copy it 100 times and put it in it's own folder. Use as boilerplate as needed.

"""




# wants output as json file. Remember some option where you can have perf output the file as json. maybe doing that for this part



import os
import json
import csv
import subprocess
import math


# data prep stage
## get all of the baseline and error injected mtx matrix files and convert them to crs
## optional function that can be called

"""
def convert_mtx_matrix_to_crs_matrix():
  path_to_mtx_matricies = os.path.join(os.getcwd(),"../../matrix_data_mtx")
  path_to_converted_crs_matricies = os.path.join(os.getcwd(),"matrix_data_crs")

  for matrix in sorted(  os.listdir(path_to_downloaded_mtx_files) ):

	if (matrix != exe_name) and (matrix != exe_name_2):

		subprocess.run( [ "sudo ./mtx2crs.py < " + matrix + " > " + path_to_converted_files + "/" + matrix + ".crs"], shell = True )


		#./mtx2crs.py < ../mat/mat_494/494_bus/494_bus.mtx > ../mat_cache/crs/494_bus.crs


"""



def get_list_of_hw_events(perf_list_output_file_name):
  subprocess.run([f" sudo perf list -j -o {perf_list_output_file_name}.json"],shell = True)




def sanitize_event_names(perf_list_output_file_name):       # "list_of_all_hw_events.json"

    event_name_arr = []

    with open(f"{perf_list_output_file_name}.json") as f:              # absolute path to json file
            contents = json.load(f)


    for dictionary in contents:

      try:
        if dictionary["EventName"] not in event_name_arr:
          event_name_arr.append( dictionary["EventName"] )
        elif dictionary["EventName"] in event_name_arr:
          continue

      except KeyError:
        continue
        """
        try:
          if dictionary["MetricGroup"] not in event_name_arr:
            event_name_arr.append( c["MetricGroup"] )
        """

    #print(len(event_name_arr))
    #print()
    #print(event_name_arr)
    return event_name_arr























"""

#num_runs = 5

max_counter = 4

matrix = "494_bus.mtx.crs"


def make_run_dir_copy_100_times():
  for file_name in os.listdir():
    if file_name.startswith("run"):
      run_name = file_name.split(".")[0]
      subprocess.run([f"mkdir {run_name}"],shell=True)
      subprocess.run([f"mv {file_name} {run_name}"],shell=True)
      os.chdir(f"{run_name}")
      for i in range(100):
        subprocess.run([f"cp {file_name} {file_name}_{i}.json"],shell=True)


      os.chdir("..")



"""









def perform_runs_on_matrix(num_runs,max_counter,event_name_arr,matrix_name):

  num_loops_needed = math.ceil( (len(event_name_arr)) / max_counter )        # take all possible y values and divide them into groups of max_counter.

  event_name_string =""

  start = 0
  end = 0

  subprocess.run([f" mkdir {matrix_name}_runs"],shell = True)

  #subprocess.run([f"cp {matrix_name} {matrix_name}_runs"],shell = True)
  #os.chdir(f"{matrix_name}_runs")


  for run_number in range(num_runs):

    #subprocess.run([f" mkdir {matrix_name}_run_{run_number}"],shell = True)

    #subprocess.run([f"touch {matrix_name}_run_{run_number}_outputs.json"],shell=True)


    for total_groups_created in range(1,(num_loops_needed+1)):
      #print(total_groups_created)
      #print(os.getcwd())

      subprocess.run([f"touch {matrix_name}_{run_number}_{total_groups_created}.json"],shell= True)

      if ( total_groups_created * max_counter ) > len(event_name_arr):
        end = end + len(event_name_arr) - start

      else:
        end = ( total_groups_created * max_counter )



      for j in range(start,end):            # division data window is the space between these running start and end values

        if j == start:             # creating event name string that will be passed to perf stat command, containing max_counter event_names
          event_name_string = event_name_string + event_name_arr[j]

        else:
          event_name_string = event_name_string +","+ event_name_arr[j]


      #os.chdir

      subprocess.run( [f"sudo perf stat -j -o {matrix_name}_{run_number}_{total_groups_created}.json -e {event_name_string}  ./crs_matmult --matrix {matrix_name} >> /dev/null"], shell = True)
      subprocess.run([f"cat {matrix_name}_{run_number}_{total_groups_created}.json >> {matrix_name}_run_{run_number}_outputs.json"],shell=True)
      subprocess.run([f"rm {matrix_name}_{run_number}_{total_groups_created}.json"],shell = True)


      if total_groups_created==(num_loops_needed):
        continue


      #print(run_number)

      #subprocess.run(["cd .."],shell = True)
      #subprocess.run([f"mv {matrix_name}_run_{run_number}_outputs.json {matrix_name}_runs"],shell = True)

      event_name_string =""
      start = end
      total_groups_created=0

    subprocess.run([f"mv {matrix_name}_run_{run_number}_outputs.json {matrix_name}_runs"],shell = True)






############################################################################################ Main



directory_with_crs_matrix_data= "matrix_data_crs_format"
perf_list_output_file_name = "list_of_all_hw_event_counters"
num_runs=2
max_counter=4


get_list_of_hw_events(perf_list_output_file_name)



sanitized_perf_list_outupt = sanitize_event_names(perf_list_output_file_name)
#print(sanitized_perf_list_outupt)


# for matrix in crs matrix data

for matrix_name in os.listdir("directory_with_crs_matrix_data"):
 os.chdir("directory_with_crs_matrix_data")
 subprocess.run([f"cp {matrix_name} .."],shell = True)
 os.chdir("..")
 perform_runs_on_matrix(num_runs,max_counter,sanitized_perf_list_outupt, matrix_name)
 subprocess.run([f"rm {matrix_name}"], shell = True)















