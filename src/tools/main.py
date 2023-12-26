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
		args = []
		super().__init__(args, desc='show CPU name and data')

	def run(self, args):
		args = self.arguments(args)
		import cpuid
		print(cpuid.get_cpu_name())
		pmu_features = cpuid.get_pmu_features()
		print(	f"PMU Architectural Version: {pmu_features.version_id}\n" \
				f"GP PMCs:                   {pmu_features.gp_pmu}\n" \
				f"GP PMCs width:             {pmu_features.gp_width}\n" \
				f"Fixed counters:            {pmu_features.f_counters}\n" \
				f"Fixed counters width:      {pmu_features.f_width}")

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

if __name__ == "__main__":
	print('[E] run adsd instead', file=stderr)
