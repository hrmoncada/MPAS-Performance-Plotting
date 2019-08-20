'''
python Henry_plot_log_p\?\?_files_5.py  ' 5 '

'''
#!/usr/bin/env python3
import re
import sys
import os
import glob
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Get the current directory path
cwd = os.getcwd()
#print("Current path folder = ",cwd,"\n")

# Folder and path   
folder = 'perf_p16_gr_openmpi'
folder_path = cwd+'/'+folder+'/'

# Script name
#print ("This is the name of the script: ", sys.argv[0],"\n")

# Create the list of file
list_of_files = glob.glob('perf_p16_gr_openmpi/log_p16_s*')
#print(list_of_files,"\n")

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

# Store variables
timer_name = []
total = []
calls = []
avg = []
timer_name_num = []
# variable label counter
i = 0 
#-------------------------------------------------------------------------------------------
# Search Patttern : Loop over the Input files list, e.g. (log_p16_s1 log_p16_s2, log_p16_s3)
#-------------------------------------------------------------------------------------------
for file_name in list_of_files:
  #print("\n", file_name)
  File = file_name.split("/") # split
  #print("Read filename  = ", File[1],"\n") # print filename
  #print() # Empty line
# file	name
  InputNameFile = File[1]

# Open the file with read only permit
  _INPUT_FILE = open(folder_path+InputNameFile, 'r')

#---------------------------------------------------- 
# Search pattern on a file
#----------------------------------------------------
  with _INPUT_FILE  as f:
      for line in f:
          match = pattern.match(line)
          if match is not None:
             _OUTPUT_FILE.write(match.group() + os.linesep)
             name = match.group()
             name = name.strip(' ')
             timer_name.append(name[6:31])
             total.append(name[55:62])  
             calls.append(name[70:80])
             avg.append(name[110:117])   
             print(name[6:31],name[55:62],name[70:73],name[110:117],len(name), i)
             i+=1  # variable label counter 
             #print(match.group())
# Close OUTPUT
_OUTPUT_FILE.close()

#----------------------------------------------------
# Plot data, Unsorted
#----------------------------------------------------
# Set the colors
#timer_name_num = list(range(0,i))
timer_name_num  = np.arange(len(timer_name[0:18]))
#print(timer_name_num)
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'g']

fig1  = plt.figure()
plt.barh(timer_name_num[0:18],total[0:18], height=0.4, align='center', color = colors)
plt.yticks(timer_name_num[0:18], timer_name[0:18])
plt.xlabel('time')
plt.ylabel('timer name')
plt.title('Layer 5 Unsorted')
plt.ylim((-1,18))
plt.grid(True)

#----------------------------------------------------
# Sorted Ascending order
#----------------------------------------------------
ttotal_avg, ttimer_name = (list(t) for t in zip(*sorted(zip(total[0:18], timer_name[0:18]))))
for j in range(0,18):
    #print("%3d   %s    %5.4f" % (j, ttimer_name[j], ttotal_avg[j]))
    print(j, ttimer_name[j], ttotal_avg[j])

#----------------------------------------------------
# Plot data, Sorted
#----------------------------------------------------
fig2 = plt.figure()
plt.barh(timer_name_num[0:18],ttotal_avg[0:18], height=0.4, align='center',  color = colors)
plt.yticks(timer_name_num[0:18], ttimer_name[0:18])
plt.xlabel('time')
plt.ylabel('timer name')
plt.title('Layer 5 - Sorted Ascending Order')
plt.ylim((-1,18))
plt.grid(True)

#----------------------------------------------------
# show the figure, but do not block
#----------------------------------------------------
plt.show()