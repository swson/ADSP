import os
import subprocess

for file_name in os.listdir():
    if file_name.endswith(".json") and file_name not in ["perf_list_output_file_name.json","list_of_all_hw_events.json"] and "run" not in file_name:

        subprocess.run([f"rm -f {file_name}"],shell=True)

    else:
        continue






