from sys import stderr

import program

@program.register_program
class matrix_downloader(program.program):
	def __init__(self):
		args = [
			('--matrix', {
					'dest':		'matrix',
					'default':	'494_bus',
					'action':	'store',
					'type':		str
				}),
			('--data-dir', {
					'dest':		'data_dir',
					'default':	'../matrices',
					'action':	'store',
					'type':		str
				})
			]
		super().__init__(args, desc="download a matrix from the matrix market")

	def run(self, args):
		args = self.arguments(args)
		import matrix_handler
		mtx = matrix_handler.matrix_handler(args.matrix, data_dir=args.data_dir)
		if not mtx.is_present():
			mtx.get_matrix()

@program.register_program
class examine_cpu(program.program):
	def __init__(self):
		args = [
			('--pmu-events', {
					'dest':		'pmu_events',
					'default':	False,
					'action':	'store_true'
				}),
			('--show-uarch', {
					'dest':		'show_uarch',
					'default':	False,
					'action':	'store_true'
				})
			]
		super().__init__(args, desc='show CPU name and data')

	def run(self, args):
		args = self.arguments(args)
		import cpuid
		print(cpuid.get_cpu_name())
		if args.pmu_events:
			pmu_features = cpuid.get_pmu_features()
			print(	f"PMU Architectural Version: {pmu_features.version_id}\n" \
					f"GP PMCs:                   {pmu_features.gp_pmu}\n" \
					f"GP PMCs width:             {pmu_features.gp_width}\n" \
					f"Fixed counters:            {pmu_features.f_counters}\n" \
					f"Fixed counters width:      {pmu_features.f_width}")
		if args.show_uarch:
			try:
				uarch = cpuid.get_microarchitecture()
				print(f'microarchitecture: {uarch.description}')
			except:
				print("[W] microarchitecture not yet recorded!")
				vendor = cpuid.get_vendor_name()
				proc_info = cpuid.processor_info()
				family, model, stepping = proc_info['family'], \
							proc_info['model'], proc_info['stepping']
				print(	f'    vendor: {vendor}, family: {family}, '
						f'model: {model}, stepping: {stepping}')

@program.register_program
class find_matrix(program.program):
	def __init__(self):
		args = [
			('--data-dir', {
					'dest':		'data_dir',
					'default':	'../matrices',
					'action':	'store',
					'type':		str
				}),
			('--info', {
					'dest':		'info',
					'default':	False,
					'action':	'store_true'
				}),
			('matrix', {
					'default':	'.*',
					'action':	'store',
					'type':		str
				})
			]
		super().__init__(args, desc='search for a matrix in the database')

	def run(self, args):
		args = self.arguments(args)
		import matrix_handler
		import csv
		import re
		matcher = re.compile(args.matrix)
		with matrix_handler.matrix_database(data_dir=args.data_dir) as db:
			for l in db:
				if matcher.match(l[1]):
					if args.info:
						collection, name, row, col, points, desc = \
							l[0], l[1], l[2], l[3], l[4], l[11]
						print(	f'name:        {name}\n' \
								f'description: {desc}\n' \
								f'collection:  {collection}\n' \
								f'rows:     {row}\n' \
								f'columns:  {col}\n' \
								f'points:   {points}\n')
					else:
						print(l[1])

@program.register_program
class perf_list(program.program):
	def __init__(self):
		args = [
			('--group', {
					'dest':		'group',
					'default':	'',
					'action':	'store',
					'type':		str
				}),
			('--info', {
					'dest':		'info',
					'default':	False,
					'action':	'store_true'
				}),
			('--verbose', {
					'dest':		'verbose',
					'default':	False,
					'action':	'store_true'
				}),
			('--perf-path', {
					'dest':		'perf_path',
					'default':	'/usr/bin',
					'action':	'store',
					'type':		str
				}),
			('--search', {
					'dest':		'search',
					'default':	None,
					'action':	'store',
					'type':		str
				})
			]
		super().__init__(args, desc='list perf events')

	def run(self, args):
		args = self.arguments(args)
		import perf_handler
		with perf_handler.perf_list(perf_path=args.perf_path, 
					verbose=args.verbose) as perf:
			if args.search:
				self.__search_events(perf, args)
			else:
				self.__dump_all_events(perf, args)

	def __dump_all_events(self, perf, args):
		for event in perf:
			if 'EventName' in event.keys():
				self.__dump_event(event, args)
			else:
				continue

	def __search_events(self, perf, args):
		import re
		matcher = re.compile(args.search)
		for event in perf:
			if 'EventName' in event.keys():
				if matcher.match(event['EventName']):
					self.__dump_event(event, args)

	def __dump_event(self, event, args):
		name = event['EventName']
		if args.info and 'BriefDescription' in event.keys():
			print(f'{name}: {event["BriefDescription"]}')
		elif args.info:
			print(f'{name}: no description available')
		else:
			print(f'{name}')

		if args.verbose and 'PublicDescription' in event.keys():
			print(f'    {event["PublicDescription"]}')
		elif args.verbose:
			print('    no long description avaliable')

if __name__ == "__main__":
	print('[E] run adsp instead', file=stderr)
