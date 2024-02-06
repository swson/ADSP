import subprocess

"""
process_1 = subprocess.Popen(["python3","get_files_from_dir.py"],stdout = subprocess.PIPE)

process_2 = subprocess.Popen(["python3","print_file_array.py"],stdin=process_1.stdout, stdout = subprocess.PIPE)
"""

subprocess.run( [ "python3 get_files_from_dir.py | python3 print_file_array.py"], shell = True)
