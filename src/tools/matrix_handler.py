from os import mkdir, path
from sys import stdout


class file_manager(object):
	@staticmethod
	def has_file(filepath, filename):
		if not path.isdir(filepath): return False
		return path.isfile(f'{filepath}/{filename}')

	@staticmethod
	def download_file(url, dst):
		def print_progress_bar(read_total, total):
			progress_width = 40
			total_rx = progress_width * read_total // total
			progress_bar = f'{"#" * (total_rx)}{" " * (progress_width - total_rx)}'
			print(f'\r[{progress_bar}] {100 * read_total / total: >6.02f}%', end='')
			stdout.flush()
	
		import urllib.request
		with urllib.request.urlopen(url) as remote:
			content_length = int(remote.getheader('Content-Length'))
			read_total = 0
			with open(dst, 'wb') as fout:
				while data := remote.read(1024):
					read_total += len(data)
					print_progress_bar(read_total, content_length)
					fout.write(data)
	
			print(' ok')

class matrix_database(object):
	__database = "http://sparse-files.engr.tamu.edu/files/{csvfile}"

	def __init__(self, data_dir='../data'):
		self.__data_dir = data_dir

	def __enter__(self):
		self.__check_matrix_database()
		self.__matrix_db_file = open(f'{self.__data_dir}/ssstats.csv')
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.__matrix_db_file.close()

	def __iter__(self):
		import csv
		reader = csv.reader(self.__matrix_db_file)
		for l in reader:
			if len(l) == 1: continue
			yield l

	def __check_matrix_database(self):
		if self.__has_matrix_database(): return
		print('[I] fetching matrix database')
		db_url = matrix_database.__database.format(csvfile="ssstats.csv")
		file_manager.download_file(db_url, f'{self.__data_dir}/ssstats.csv')

	def __has_matrix_database(self):
		return file_manager.has_file(self.__data_dir, 'ssstats.csv')

class matrix_handler(object):
	__base_url = "https://suitesparse-collection-website.herokuapp.com/MM/{collection}/{matrix}.tar.gz"

	def __init__(self, mtx, data_dir='../data'):
		self.__mtx = mtx
		self.__data_dir = data_dir

	def is_present(self):
		return file_manager.has_file(self.__data_dir, f'{self.__mtx}.tar.gz')

	def get_matrix(self):
		filename = f'{self.__data_dir}/{self.__mtx}.tar.gz'
		if not path.isdir(self.__data_dir): mkdir(f'{self.__data_dir}')

		collection = self.__find_collection()
		if not collection: raise Exception(f"matrix not found in collection")

		matrix_url = matrix_handler.__base_url.format(collection=collection, matrix=self.__mtx)

		print('[I] fetching matrix')
		file_manager.download_file(matrix_url, filename)

	def __enter__(self):
		if not self.is_present(): self.get_matrix()
		import tarfile
		self.__tarfile = tarfile.open(f'{self.__data_dir}/{self.__mtx}.tar.gz', 'r:gz')
		self.__mtx_file_data = self.__tarfile.extractfile(f'{self.__mtx}/{self.__mtx}.mtx')
		return self
		
	def __iter__(self):
		for l in self.__mtx_file_data:
			yield l.decode('utf-8')[:-1]

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.__tarfile.close()


	def __find_collection(self):
		# GRR... so the matrices are found within collections and sorted
		# alphabetically in the collection... we have to scan the file until we
		# find the collection itself :/
		with matrix_database(data_dir=self.__data_dir) as db:
			for l in db:
				if l[1] == self.__mtx: return l[0]
		# import csv
		# with open(f'{self.__data_dir}/ssstats.csv') as f:
		# 	reader = csv.reader(f)
		# 	for l in reader:
		# 		if len(l) == 1: continue
		# 		if l[1] == self.__mtx: return l[0]
		# return None


