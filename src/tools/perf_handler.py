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
					*perf_list.__perf_args.split()]
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
	__perf_cmd = 'perf'
	__perf_subcmd = 'stat'
	__perf_args = '-x {separator}'
	__perf_events = '-e {events}'

	def __init__(self, cmd, events=None, separator='|', perf_path='/usr/bin'):
		self.__cmd = cmd
		self.__separator = separator
		self.__perf_path = perf_path
		self.__events = events
		self.__perf_process = None
		self.__perf_process_cmd = None

	@property
	def perf_command(self):
		return self.__perf_process_cmd

	@property
	def return_value(self):
		if self.__perf_process:
			return self.__perf_process.wait()
		return None

	def __enter__(self):
		import subprocess
		perf_args = perf_stat.__perf_args.format(separator=self.__separator)

		perf = [f'{self.__perf_path}/{perf_stat.__perf_cmd}',
					perf_stat.__perf_subcmd,
					*perf_args.split()]
		if self.__events:
			perf.extend(perf_stat.__perf_events.format(events=','.join(self.__events)).split())
		perf.extend(self.__cmd)
		sellf.__perf_process_cmd = " ".join(perf)
		self.__perf_process = subprocess.Popen(args=perf,
				stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		return self

	def __iter__(self):
		out = self.__perf_process.stderr.read().decode('utf-8').split('\n')
		for l in out:
			yield l

	def __exit__(self, exc_type, value, traceback):
		pass
