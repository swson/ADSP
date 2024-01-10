from sys import stderr


class perf_handler(object):
	__perf_map_file = "mapfile.csv"

	def __init__(self, cpuinfo=None, perf_data_dir=None, perf_version=None):
		self.__perf_data_dir = perf_data_dir
		self.__perf_version = perf_version
		self.__uarch = uarch
		self.__find_microarchitecture()
		

	def __find_microarchitecture(self):
		import csv, re
		if not self.__uarch:
			import cpuid
			vendor = cpuid.get_vendor_name()
			cpuinfo = cpuid.get_processor_info()
			# XXX: cascadelakex and skylakex use a different pattern?
			self.__uarch = f'{vendor}-{cpuinfo.family:01X}-{cpuinfo.model:02X}'
		with open(f'{perf_data_dir}/{perf_handler.__perf_map_file}') as f:
			reader = csv.DictReader(f, delimiter=',')
			for entry in reader:
				if re.match(entry['Family-model'], self.__uarch):
					self.__uarch_data = entry
					return
		raise Exception('unable to determine microarchitecture')


class perf_list(object):
	__perf_cmd = 'perf'
	__perf_subcmd = 'list'
	__perf_args = '--json'

	def __init__(self, perf_path='/usr/bin', verbose=False):
		self.__perf_path = perf_path
		self.__verbose = verbose

	def __enter__(self):
		import subprocess
		perf = [f'{self.__perf_path}/{perf_list.__perf_cmd}',
					perf_list.__perf_subcmd,
					perf_list.__perf_args]
		if self.__verbose: perf.append(' --long-desc')
		self.__perf_process = subprocess.Popen(args=perf, stdout=subprocess.PIPE)
		return self

	def __iter__(self):
		import json
		out = self.__perf_process.stdout.read().decode('utf-8')
		# perf embeds this thing in stdout instead of stderr... go figure...
		err_message  = 'Error: failed to open tracing events directory'
		if out.find(err_message) >= 0:
			print('[W] some PMU can not probed, run as root for full list')
			out = out.replace(f'{err_message}\n', '')
		for l in json.loads(out):
			yield l
		

	def __exit__(self, exc_type, value, traceback):
		pass
		

class perf_stat(object):
	def __init__(self):
		pass

	def __enter__(self):
		pass

	def __exit__(self, exc_type, value, traceback):
		pass
