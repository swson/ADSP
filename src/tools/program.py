from abc import abstractmethod


class program(object):
	def __init__(self, args, desc=None):
		from argparse import ArgumentParser
		self.__parser = ArgumentParser(prog=self.__class__.__name__,
					description=desc)
		for param, arg in args:
			self.__parser.add_argument(param, **arg)

	@property
	def description(self):
		return self.__parser.description

	def arguments(self, args):
		return self.__parser.parse_args(args)

	@abstractmethod
	def run(self, args):
		pass

	def __call__(self, args):
		self.run(args)

	def __repr__(self):
		return f'{self.__class__.__name__}'

	def __str__(self):
		return f'{self.__class__.__name__}'


__programs = dict()

def register_program(tgt_class):
	__programs[tgt_class.__name__] = tgt_class()

def get_programs():
	return __programs
