import os
import json
import subprocess
import math

max_counter = 4
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

def perform_run(matrix_file, batch_id, num_runs, max_counter, event_name_arr):
    num_loops_needed = math.ceil(len(event_name_arr) / max_counter)
    matrix_basename = os.path.basename(matrix_file)
    base_name = os.path.join(output_dir, f"{matrix_basename}_{batch_id + 1}")

    event_name_string = ""
    output_file = f"{base_name}.json"
    subprocess.run([f"touch {output_file}"], shell=True)

    start = 0
    end = 0

    for run_number in range(num_runs):
        for total_groups_created in range(1, num_loops_needed + 1):
            print(f"[Batch {batch_id}] Run {run_number}, Group {total_groups_created}")

            if (total_groups_created * max_counter) > len(event_name_arr):
                end = end + len(event_name_arr) - start
            else:
                end = total_groups_created * max_counter

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

            subprocess.run([perf_cmd], shell=True)
            subprocess.run([f"cat {json_output} >> {output_file}"], shell=True)

            if total_groups_created == num_loops_needed:
                continue

            event_name_string = ""
            start = end

############## Main ##############

list_of_all_hw_events = "list_of_all_hw_events.json"
subprocess.run([f"sudo perf list -j -o {list_of_all_hw_events}"], shell=True)

temp = get_event_names(list_of_all_hw_events)

input_files = sorted([
    os.path.join(input_dir, f)
    for f in os.listdir(input_dir)
    if f.startswith("494_bus_point_gauss_") and f.endswith(".crs")
])

for matrix_file in input_files:
    for batch_id in range(1):  # only one run per matrix
        perform_run(matrix_file, batch_id, 1, max_counter, temp)
