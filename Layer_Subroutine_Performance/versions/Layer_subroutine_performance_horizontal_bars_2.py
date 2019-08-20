'''
https://www.quora.com/How-do-I-write-a-python-script-that-will-find-a-specific-string-in-a-txt-file-select-the-rest-of-string-surrounding-it-and-paste-in-another-txt

Compile, input argument sys.argv[1] = ' 5 '
$ python3 Henry_plot_log_p\?\?_files_2.py ' 5 '

'''
#!/usr/bin/env python3

import re
import sys
import os 

# get the current directory path
cwd = os.getcwd()
print("Current path folder = ",cwd)

# Script name
print ("This is the name of the script: ", sys.argv[0])

# Folder and files	name   
folder = 'perf_p16_gr_openmpi'  
InputNameFile = 'log_p16_s1'
OutputNameFile = 'File_Output.txt'
full_folder_path = cwd+'/'+folder+'/'

#cwd = os.getcwd()
print("full path to file  = ",full_folder_path)
# Print input file name
print("File name =",InputNameFile,"\n")

# Open the file with read only permit
_INPUT_FILE = open(full_folder_path + InputNameFile, 'r')

# Open the file with write only permit
_OUTPUT_FILE = open(full_folder_path + OutputNameFile, 'w')

# write line-labels
labels = '    timer_name                                            total       calls        min            max            avg      pct_tot   pct_par     par_eff:q'

_OUTPUT_FILE.write(labels + os.linesep)
print(labels)

# Define Main function
def main():
# Input pattern to be search 
   pattern = re.compile('^(.*)' + re.escape(sys.argv[1]) + '(.*)$')

#  Search pattern
   with _INPUT_FILE as f:
      for line in f:
          match = pattern.match(line)
          if match is not None:
            print(match.group())
            _OUTPUT_FILE.write(match.group() + os.linesep)
   _OUTPUT_FILE.close()

# Main        
if __name__ == '__main__':
      main()
