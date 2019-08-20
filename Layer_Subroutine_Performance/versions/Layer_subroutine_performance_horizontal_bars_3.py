'''
https://www.quora.com/How-do-I-write-a-python-script-that-will-find-a-specific-string-in-a-txt-file-select-the-rest-of-string-surrounding-it-and-paste-in-another-txt

Compile, input argument sys.argv[1] = ' 5 '
$ python3 Henry_plot_log_p\?\?_files_2.py ' 5 '


'''

#!/usr/bin/env python3

import re
import sys
import os 
import glob

# Get the current directory path
cwd = os.getcwd()
print("Current path folder = ",cwd,"\n")

# Script name
print ("This is the name of the script: ", sys.argv[0],"\n")

# Folder and path   
folder = 'perf_p16_gr_openmpi'  
folder_path = cwd+'/'+folder+'/'

# Search multiple filenames
filenames = sorted(glob.glob(folder +"/"+ 'log_p16_s*'))
filenames = filenames[0:3]
#print(filenames,"\n")

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

# Define Main Function
def main():
# Search match pattern on Files
	for i in range(3):
		print("\n", filenames[i])
		File = filenames[i].split("/") # split
		print("Read filename  = ", File[1],"\n") # print filename

# file	name     
		InputNameFile = File[1]

# Open the file with read only permit
		_INPUT_FILE = open(folder_path+InputNameFile, 'r')

#  Search pattern
		with _INPUT_FILE as f:
		    for line in f:
		       match = pattern.match(line)
		       if match is not None:
		          _OUTPUT_FILE.write(match.group() + os.linesep)
		          print(match.group())

# Close OUTPUT
	_OUTPUT_FILE.close()

# Main        
if __name__ == '__main__':
      main()
