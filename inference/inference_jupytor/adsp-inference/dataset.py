#!/usr/bin/env python

"""
This script analyzes the output of the cloudlab dataset into CSV format

Usage: ./analyze.py 494_bus 5
"""

import sys
import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Dataset:
    def __init__(self, data_path, mat_name="494_bus", nruns=5):
        self.labels = []
        self.data = {}

        clean_data = Dataset.process_runs(data_path, mat_name, 0, 0, nruns)
        for events in clean_data:
            if events in self.data:
                self.data[events].append(clean_data[events])
            else:
                self.data[events] = [clean_data[events]]

        self.labels.append((0.0, 0.0))


        # Add: process (0.0, 0.01 ~ 0.99)
        for inj_rate in [i / 100 for i in range(1, 100)]:
            d = Dataset.process_runs(data_path, mat_name, 0.0, inj_rate, nruns)
            for events in d:
                if events in self.data:
                    self.data[events].append(d[events])
                else:
                    self.data[events] = [d[events]]
            self.labels.append((0.0, inj_rate))


        inj_rates = [i / 100 for i in range(1, 11)]
        err_rates = [i / 100 for i in range(1, 11)]

        for err_rate in err_rates:
            for inj_rate in inj_rates:
                d = Dataset.process_runs(data_path, mat_name, err_rate, inj_rate, nruns)
                for events in d:
                    if events in self.data:
                        self.data[events].append(d[events])
                    else:
                        self.data[events] = [d[events]]
                self.labels.append((err_rate, inj_rate))

        self.__gen_dataframe()

    @staticmethod
    def process_runs(data_dir, mat_name, err_rate, inj_rate, nruns):
        # Loop through each run
        data = {}
        for run in range(1, nruns+1):
            
            fp ="{}_gauss_{:.2f}_{:.2f}.mtx_{}.json".format(mat_name, err_rate, inj_rate, run)
            fp = os.path.join(data_dir, fp)

            with open(fp, "r") as f:
                for line in f.readlines():
                    d = json.loads(line)
                    event = d["event"]
                    try:
                        val = float(d["counter-value"])
                    except ValueError:
                        val = 0
                    if event in data:
                        data[event].append(val)
                    else:
                        data[event] = [val]
        # Take the average of counter values across all runs
        for d in data:
            data[d] = sum(data[d]) / len(data[d])

        return data

    def __gen_dataframe(self):
        expected_len = len(self.labels)
        clean = [k for k, v in self.data.items() if len(v) != expected_len]
        for k in clean:
            del self.data[k]


        index = []
        for (i, e) in self.labels:
            index.append(f"{i}_{e}")

        self.df = pd.DataFrame.from_dict(self.data)
        self.df.index = index

if __name__ == "__main__":
    DATA_DIR = os.path.abspath("494_bus")

    d = Dataset(DATA_DIR)
    print(d.df.head())
