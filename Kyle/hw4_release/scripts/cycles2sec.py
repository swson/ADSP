#! /usr/bin/python

import argparse
from sys import stdin

# by default, we will try to get CPU data dynamically
parser = argparse.ArgumentParser(prog='PROG')
parser.add_argument('--cpufreq', '-f', action='store', type=float, default=0)
args = parser.parse_args()

cpufreq = float(args.cpufreq)

if cpufreq == 0:
	import cpuinfo
	cpufreq = (cpuinfo.get_cpu_info()['hz_advertised_raw'][0])

for line in stdin:
	print(float(line)/cpufreq)

