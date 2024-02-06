from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument("list_of_file_names",type = str)

args = parser.parse_args()

print(args.list_of_file_names)
