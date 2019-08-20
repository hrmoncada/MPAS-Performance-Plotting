'''
https://stackoverflow.com/questions/208120/how-to-read-and-write-multiple-files

$ python example_2_glob_glob.py ' 5 ' 

'''
#!/usr/bin/env python3
import re
import sys
import os
import glob

# Get the current directory path
cwd = os.getcwd()
print("Current path folder = ",cwd,"\n")

# Folder and path   
folder = 'perf_p16_gr_openmpi'
folder_path = cwd+'/'+folder+'/'

# Script name
print ("This is the name of the script: ", sys.argv[0],"\n")

# Create the list of file
list_of_files = glob.glob('perf_p16_gr_openmpi/log_p16_s*')
print(list_of_files,"\n")

# Open the OUTPUT file with write only permit
OutputNameFile = 'File_Output.txt'
_OUTPUT_FILE = open(folder_path + OutputNameFile, 'w')

# OUTPUT file, write line-labels
labels = '    timer_name                                            total       calls        min            max            avg      pct_tot   pct_par     par_eff:q'

# Write label
_OUTPUT_FILE.write(labels + os.linesep)
print(labels)

# Input pattern to be search
pattern = re.compile('^(.*)' + re.escape(sys.argv[1]) + '(.*)$')

# Loop over the list files
for file_name in list_of_files:
  print("\n", file_name)
  File = file_name.split("/") # split
  print("Read filename  = ", File[1],"\n") # print filename
# file	name
  InputNameFile = File[1]

# Open the file with read only permit
  _INPUT_FILE = open(folder_path+InputNameFile, 'r')

# Search pattern
  with _INPUT_FILE  as f:
      for line in f:
          match = pattern.match(line)
          if match is not None:
             _OUTPUT_FILE.write(match.group() + os.linesep)
             print(match.group())

# Close OUTPUT
_OUTPUT_FILE.close()
