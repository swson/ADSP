#!/bin/bash                                                                                                                                                                                                  
target_dir="output_point_gauss_all_avg/bcsstk20_4"

for f in "$target_dir"/*.mtx.crs_*; do
  newname="${f/.mtx.crs_/.mtx_}"
  mv "$f" "$newname"
done
