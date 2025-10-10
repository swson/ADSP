#! /user/bin/bash

run_num=1

num_groups_needed=9

touch run_${run_num}_outputs.json

for i in {1..9} #change 9 to your max number of total groups created
do

    cat 494_bus.mtx.crs_0_$i.json >> run_${run_num}_outputs.json
done


python3 remove_json_files_for_testing.py
