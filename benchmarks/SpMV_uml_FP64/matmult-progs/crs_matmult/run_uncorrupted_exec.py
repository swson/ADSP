


# total number of runs
# perf options
# make sure I am using the right machine in cloudlab
# actual raw 494 bus data that was just converted to crs... non zero status ? does that make a difference ?


# wants output as json file. Remember some option where you can have perf output the file as json. maybe doing that for this part



import os
import json
import csv
import subprocess
import math


#num_runs = 5

max_counter = 4

matrix = "/input/494_bus_input/494_bus.mtx.crs"


def get_event_names(json_file_containing_all_events_for_cpu):

    event_name_arr = []



    with open(json_file_containing_all_events_for_cpu) as f:              # absolute path to json file
        contents = json.load(f)


    for dictionary in contents:
        try:
            name = dictionary["EventName"]

            if (
                name not in event_name_arr and
                "..." not in name and 
                "rNNN" not in name and
                not name.startswith("msr/") and
                "modifier" not in name and
                "uncore" not in name and
                "N/A" not in name and
                "//" not in name
            ):
                event_name_arr.append(name)
                
        except KeyError:
            continue
        """
        try:
          if dictionary["MetricGroup"] not in event_name_arr:
            event_name_arr.append( c["MetricGroup"] )
        """

    return event_name_arr





def perform_run(batch_id, num_runs,max_counter,event_name_arr):




  #num_loops_needed = math.ceil( (len(event_name_arr)/100) / max_counter )        # take all possible y values and divide them into groups of max_counter.
  num_loops_needed = math.ceil( (len(event_name_arr)) / max_counter )        # take all possible y values and divide them into groups of max_counter.
  base_name = f"output/494_bus_point_gauss_0.00_0.{batch_id + 1}.mtx_1"
  os.makedirs("output", exist_ok=True)

  event_name_string =""

  output_file = f"{base_name}.json"
  subprocess.run([f"touch {output_file}"], shell=True)

  
  start = 0
  end = 0

  #print("number of groups needed in combine_into_one_jason_file.sh: ", num_loops_needed, "\n")


  for run_number in range(num_runs):

    subprocess.run([f"touch run_batch{batch_id}_run_{run_number}_outputs.json"],shell=True)

    #subprocess.run([f"mkdir {matrix}_{run_number}"],shell = True)



    for total_groups_created in range(1,(num_loops_needed+1)):
      print(total_groups_created)


      if ( total_groups_created * max_counter ) > len(event_name_arr):

        end = end + len(event_name_arr) - start

      else:

        end = ( total_groups_created * max_counter )




      for j in range(start,end):            # division data window is the space between these running start and end values


        if j == start:             # creating event name string that will be passed to perf stat command, containing max_counter event_names

          event_name_string = event_name_string + event_name_arr[j]


        else:
          event_name_string = event_name_string +","+ event_name_arr[j]




      #data_window_event_name_arr_subset = event_name_string.split(',')

      #print(event_name_string)
      #print()



      #try:

      json_output = f"{base_name}_{total_groups_created}.json"
      perf_cmd = (
          f"sudo perf stat -j -o {json_output} -e {event_name_string} "
          f"./crs_matmult --matrix {matrix} >> /dev/null"
      )

      
      subprocess.run( [perf_cmd], shell = True)
      subprocess.run([f"cat {json_output} >> {output_file}"],shell=True)

      if total_groups_created==(num_loops_needed):
        continue

        #subprocess.run([f"mv {matrix}_{run_number}.json {matrix}_{run_number}"])
        #subprocess.run( [f"sudo perf stat -j -e {event_name_string}  ./crs_matmult --matrix {matrix} >> /dev/null"], shell = True)
      #except:
        #continue


      event_name_string =""
      start = end
      total_groups_created=0



    #subprocess.run(["sudo bash combine_into_one_json_file.sh"],shell = True)
    #combine_into_one_jason_file(num_loops_needed,run_number)













############################################################################################ Main



list_of_all_hw_events = "list_of_all_hw_events.json"

subprocess.run([f"sudo perf list -j -o {list_of_all_hw_events}"],shell = True)




temp =get_event_names(list_of_all_hw_events)

for batch_id in range(100):
  temp2 = perform_run(batch_id,1,4,temp)














