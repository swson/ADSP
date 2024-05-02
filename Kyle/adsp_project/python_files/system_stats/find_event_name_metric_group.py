import csv
import json
import subprocess

perf_list_output_json = "perf_list_output.json"

subprocess.run(["sudo perf list -j > " + perf_list_output_json], shell=True)


def write_dict_to_csv(file_name,temp_dict_list):

    field_names = []

    for d in temp_dict_list:

        for k in d.keys():

            if k not in field_names:
                field_names.append(k)
            else:
                continue


    with open(file_name, 'w') as output_csv_file:

        writer = csv.DictWriter(output_csv_file, fieldnames=field_names)
        writer.writeheader()

        for data_dict in temp_dict_list:
            writer.writerow(data_dict)


# main

with open(perf_list_output_json) as json_file:

    data = json_file.read()


json_data = json.loads(data)




event_data_dict_list = []
metric_data_dict_list = []

for d in json_data:     # gong through each dictionary in the json_data list of dictionaries

    for k in d.keys():  # checking the keys in each dictionary for a specific key used to categorize them

        if k == "EventName":       

            event_data_dict_list.append(d) 
            break
        
        elif k == "MetricGroup":
            
            metric_data_dict_list.append(d)
            break

        else:
            continue

        

write_dict_to_csv("event_csv.csv",event_data_dict_list)

write_dict_to_csv("metric_csv.csv",metric_data_dict_list)




























