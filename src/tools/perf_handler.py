from sys import stderr
import cpuid


class perf_handler(object):
	def __init__(self, microarch=None):
		self._microarch = self.__check_microarch(microarch)


	def __check_microarch(self, uarch):
		cpu = cpuid.get_microarchitecture()
		if uarch and uarch != cpu.directory:
			print(f'[W] directory mismatch on probed microarchitecture, using {uarch}', file=stderr)
			return uarch
		print(f'[I] autodetected microarchitecture {cpu.directory}')
		return cpu.directory
