import os
import json
import subprocess
import math
from pathlib import Path

max_counter = 4
batch_id2 = 0  

matrix = "input/494_bus_input/494_bus.mtx.crs" 
input_dir = "input/494_bus_input"
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

def get_event_names(json_file_containing_all_events_for_cpu):
    event_name_arr = []
    with open(json_file_containing_all_events_for_cpu) as f:
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
    return event_name_arr

def perform_run_error(matrix_file, batch_id, num_runs, max_counter, event_name_arr):

    num_loops_needed = math.ceil(len(event_name_arr) / max_counter)
    matrix_basename = os.path.basename(matrix_file)
    base_name = os.path.join(output_dir, f"{matrix_basename}_{batch_id + 1}")

    output_file = f"{base_name}.json"
    Path(output_file).touch()

    for run_number in range(num_runs):

        start = 0
        end = 0

        for total_groups_created in range(1, num_loops_needed + 1):
            print(f"[Batch {batch_id}] (ERROR) Run {run_number}, Group {total_groups_created}")

            if (total_groups_created * max_counter) > len(event_name_arr):
                end = start + (len(event_name_arr) - start)
            else:
                end = total_groups_created * max_counter

            event_name_string = ""
            for j in range(start, end):
                if j == start:
                    event_name_string = event_name_arr[j]
                else:
                    event_name_string += "," + event_name_arr[j]

            json_output = f"{base_name}_{total_groups_created}.json"
            perf_cmd = (
                f"sudo perf stat -j -o {json_output} -e {event_name_string} "
                f"./crs_matmult --matrix {matrix_file} >> /dev/null"
            )
            subprocess.run([perf_cmd], shell=True, check=False)
            subprocess.run([f"cat {json_output} >> {output_file}"], shell=True, check=False)


            start = end

def perform_run(batch_id, num_runs, max_counter, event_name_arr):

    num_loops_needed = math.ceil(len(event_name_arr) / max_counter)
    base_name = f"{output_dir}/494_bus_point_gauss_0.00_0.{batch_id + 1}.mtx_1"
    os.makedirs(output_dir, exist_ok=True)

    output_file = f"{base_name}.json"
    Path(output_file).touch()

    for run_number in range(num_runs):
        Path(f"run_batch{batch_id}_run_{run_number}_outputs.json").touch()


        start = 0
        end = 0

        for total_groups_created in range(1, num_loops_needed + 1):
            print(f"[Batch {batch_id}] (CLEAN) Run {run_number}, Group {total_groups_created}")

            if (total_groups_created * max_counter) > len(event_name_arr):
                end = start + (len(event_name_arr) - start)
            else:
                end = total_groups_created * max_counter

            event_name_string = ""
            for j in range(start, end):
                if j == start:
                    event_name_string = event_name_arr[j]
                else:
                    event_name_string += "," + event_name_arr[j]

            json_output = f"{base_name}_{total_groups_created}.json"
            perf_cmd = (
                f"sudo perf stat -j -o {json_output} -e {event_name_string} "
                f"./crs_matmult --matrix {matrix} >> /dev/null"
            )

            subprocess.run([perf_cmd], shell=True, check=False)
            subprocess.run([f"cat {json_output} >> {output_file}"], shell=True, check=False)

            start = end

############## Main ##############

list_of_all_hw_events = "filtered_events.json"
subprocess.run([f"sudo perf list -j -o {list_of_all_hw_events}"], shell=True)

temp = get_event_names(list_of_all_hw_events)

input_files = sorted([
    os.path.join(input_dir, f)
    for f in os.listdir(input_dir)
    if f.startswith("494_bus_point_gauss_") and f.endswith(".crs")
])

for batch_id2 in range(100):
    perform_run(batch_id2, 1, max_counter, temp)

for matrix_file in input_files:
    for batch_id in range(1):
        perform_run_error(matrix_file, batch_id, 1, max_counter, temp)


#for matrix_file in input_files:
#    for batch_id in range(1):
#        perform_run(batch_id2, 1, max_counter, temp)
#        perform_run_error(matrix_file, batch_id, 1, max_counter, temp)
#        batch_id2 += 1


