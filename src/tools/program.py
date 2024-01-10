from abc import abstractmethod


class program(object):
	def __init__(self, argslist, args=None, desc=None):
		from argparse import ArgumentParser
		self.__parser = ArgumentParser(prog=self.__class__.__name__,
					description=desc)
		for param, arg in argslist:
			self.__parser.add_argument(param, **arg)

		self.__arguments = self.__parser.parse_args(args)

	@property
	def description(self):
		return self.__parser.description

	@property
	def arguments(self):
		return self.__arguments

	@abstractmethod
	def run(self):
		pass

	def __call__(self):
		self.run()

	def __repr__(self):
		return f'{self.__class__.__name__}'

	def __str__(self):
		return f'{self.__class__.__name__}'


__programs = dict()

def register_program(tgt_class):
	__programs[tgt_class.__name__] = tgt_class

def get_programs():
	return __programs
