#!/usr/bin/env python3

"""
This script processes the output of raw HPCG runs into a CSV dataset
"""

import os
import shutil
from glob import glob
import pandas as pd

class DataSet:
    def __init__(self, data_dir="raw", out_dir="data"):
        self.funcs = ["cg", "mg_ref", "cg_ref", "spv_ref", "cg_timed"]
        self.files = {}
        self.data = {}
        self.out_dir = out_dir
        self.data_dir = data_dir
        print(f"data_dir: {data_dir}")
        shutil.rmtree(self.out_dir, ignore_errors=True)
        
        print(f"before process_dir")
        self.process_dir(data_dir)
        self.write_files()
        self.to_csv()

    def process_dir(self, data_dir):
        for grid_folder in os.listdir(data_dir):
            if grid_folder.startswith("grid-"):
                grid_size = int(grid_folder.split("-")[1])
                print(f"grid folder: {grid_folder}, grid size: {grid_size}")

                folder_path =  os.path.join(data_dir, grid_folder)

                for filename in os.listdir(folder_path):
                    if filename.endswith(".txt"):
                        file_path = os.path.join(folder_path, filename)
                        self.process_file(file_path, grid_size)
    

    def process_file(self, path, g, core=True):
        b = os.path.basename(path)
        if b.lower()[:4] != "hpcg":
            if core:
                s = b.split("_core_0_")
            else:
                s = b.split("_uncore_0_")
            func = s[0]
            err_rate = float(s[1].split("_")[0])
            inj_rate = float(s[1].split("_")[1].split(".txt")[0])
            key = (func, g, err_rate, inj_rate)
            print(f"func: {func}, grid: {g}, err_rate: {err_rate}, inj_rate: {inj_rate}")
            if key in self.files:
                self.files[key].append(path)
            else:
                self.files[key] = [path]

    def write_files(self):
        os.makedirs(self.out_dir)
        for (k, v) in self.files.items():
            (func, g, err_rate, inj_rate) = k
            for i, file in enumerate(v):
                e_str = f"{err_rate:{1}.{2}f}"
                i_str = f"{inj_rate:{1}.{2}f}"
                f = f"{func}_{g}_{e_str}_{i_str}_{i}.txt"
                dst = os.path.join(self.out_dir, f)
                shutil.copyfile(file, dst)

    def to_csv(self):
        grid_size = 494
        for f in self.funcs:
            data = {'ErrorRate': [], "InjectionRate": []}
            for err_rate in range(0, 11):
                err_rate /= 10
                estr =  f"{err_rate:.2f}"
                for inj_rate in range(0, 11):
                    inj_rate /= 100
                    istr =  f"{inj_rate:.2f}"
                    pattern = f"{f}_{grid_size}_{estr}_{istr}_*.txt"
                    files = glob(os.path.join(self.out_dir, pattern))
                    for file in files:
                        counters = self.read_data(file, f, err_rate, inj_rate)
                        data["ErrorRate"].append(err_rate)
                        data["InjectionRate"].append(inj_rate)
                        for k, v in counters.items():
                            data.setdefault(k, []).append(v)
            df = pd.DataFrame.from_dict(data)
            title = f"{f}_{grid_size}"
            df.to_csv(os.path.join(self.out_dir, f"{title}.csv"), index=False)

    def read_data(self, file, func, err_rate, inj_rate):
        with open(file, "r") as f:
            lines = [line.strip() for line in f.readlines()]

        counters = {}
        for line in lines:
            key, val = line.split(" ")
            if key in counters:
                raise Exception("Duplicate key found in file")
            counters[key] = int(val, base=10)
        return counters

if __name__ == "__main__":
    d = DataSet()
