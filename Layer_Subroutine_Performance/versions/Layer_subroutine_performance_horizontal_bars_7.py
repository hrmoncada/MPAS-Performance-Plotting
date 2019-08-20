'''
python Henry_plot_log_pfiles_7.py  ' 5 '

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

# Get the files and Folder-path   
folder = 'perf_p16_gr_openmpi'
folder_path = cwd+'/'+folder+'/'

# Script name
#print ("This is the name of the script: ", sys.argv[0],"\n")

# Create the list of files
list_of_files = glob.glob('perf_p16_gr_openmpi/log_p16_s*')
print(list_of_files,"\n")

# Open the _OUTPUT_FILE with write only permit
OutputNameFile = 'File_Output.txt'
_OUTPUT_FILE = open(folder_path + OutputNameFile, 'w')

# Label line write in _OUTPUT_FILE
labels = 'Layer    timer_name                                        total       calls        min            max            avg      pct_tot   pct_par     par_eff    i'
#print(labels)

# Write "labels" into _OUTPUT_FILE
_OUTPUT_FILE.write(labels + os.linesep)

# Input pattern to be search on the _INPUT_FILE
pattern = re.compile('^(.*)' + re.escape(sys.argv[1]) + '(.*)$')

#----------------------------------------------------
# Store Variables
#----------------------------------------------------
timer_name = []
total = []
calls = []
avg = []
timer_name_num = []
count = []

#-------------------------------------------------------------------------------------------
# Search Patttern : Loop over the Input files list, e.g. (log_p16_s1 log_p16_s2, log_p16_s3)
#-------------------------------------------------------------------------------------------
for file_name in list_of_files:
  #print("\n", file_name)
  File = file_name.split("/") # split "perf_p16_gr_openmpi/log_p16_s = perf_p16_gr_openmpi + log_p16_s  = File[0] + File[1]"
  #print("Read filename  = ", File[1],"\n") # print filename
  #print() # Empty line
  
# file	name
  InputNameFile = File[1]

# Open the file with read only permit
  _INPUT_FILE = open(folder_path + InputNameFile, 'r')

# Variable label counter , update  
  i = 0  
#---------------------------------------------------- 
# Search pattern on a file
#----------------------------------------------------
  with _INPUT_FILE  as f:
      for line in f:
          match = pattern.match(line)
          if match is not None:
             _OUTPUT_FILE.write(match.group() + os.linesep)# Save information
             name = match.group()                          #
             #print(match.group() + '      ' + str (i))    # Print all columns (0 to 8)
             name = name.strip(' ')                        # Split columns
             timer_name.append(name[6:31])                 # Store timer_name (col 1)
             total.append(name[55:62])                     # Store total (col 2)
             calls.append(name[70:73])                     # Store calls (col 3) = Number of times a funciton was called
             avg.append(name[110:117])                     # Store avg   (col 6) = Average time
             count.append(i)                               # Store variable index counter
            #print(name[6:31],name[55:62],name[70:73],name[110:117],len(name), i) # print require variables
             i+=1  # Variable label counter, increment 

# Close _OUTPUT_FILE
_OUTPUT_FILE.close()

print("perf_p16_gr_openmpi/log_p16_s-LENGTH = %d"% i)
print ("Unsorted output")
print (" ")

# Open the OUTPUT file with write only permit
OutputNameFileAvg = 'File_Output_Avg.txt'
_OUTPUT_FILE_AVG = open(folder_path + OutputNameFileAvg, 'w')

# Label line write in _OUTPUT_FILE_AVG
label_avg = '  j      timer_name             avg_total vag_calls  avg_avg'
_OUTPUT_FILE_AVG.write(label_avg + os.linesep)
print(label_avg)

#----------------------------------------------------
# Store Variables
#----------------------------------------------------
ttimer_name = []
ttotal_avg = []
tcalls_avg = []
tavg_avg = []
count_avg = []
#----------------------------------------------------
# Calculate Average Values
#----------------------------------------------------
for j in range(0,i):
   ttimer_name.append(timer_name[j])
   total_avg = ( float(total[j]) + float(total[j+i]) + float(total[j+2*i]) )/3
   ttotal_avg.append(total_avg)
   calls_avg = ( float(calls[j]) + float(calls[j+i]) + float(calls[j+2*i]) )/3
   tcalls_avg.append(calls_avg)
   avg_avg = ( float(avg[j]) + float(avg[j+i]) + float(avg[j+2*i]) )/3
   tavg_avg.append(avg_avg) 
   count_avg.append(j)    # Store variable index counter
   print("%3d   %s    %5.3f    %5.1f     %5.3f" % (j, ttimer_name[j], ttotal_avg[j], tcalls_avg[j], tavg_avg[j]))
   _OUTPUT_FILE_AVG.write("%3d   %s    %5.3f    %5.1f     %5.3f\n" % (j, ttimer_name[j], ttotal_avg[j], tcalls_avg[j], tavg_avg[j]))
   
# Close OUTPUT
_OUTPUT_FILE_AVG.close()

#----------------------------------------------------
# Plot data, Unsorted
#----------------------------------------------------
# Set the colors
#timer_name_num = list(range(0,i))
timer_name_num  = np.arange(len(ttimer_name))
#print(timer_name_num)
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'g']

fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharey=False)
# subplot 211
ax1.barh(timer_name_num[0:18],ttotal_avg[0:18],  height=0.4, align='center', color = colors)
ax1.set_yticks(timer_name_num)
ax1.set_yticklabels(ttimer_name[0:18])
ax1.set_xlabel('time')
ax1.set_ylabel('timer name')
ax1.set_title('Layer 5 - Unsorted')
ax1.set_ylim((-1,18))
ax1.grid(True)
print (" ")

#----------------------------------------------------
# Sorted Ascending order
#----------------------------------------------------
# Label line write in _OUTPUT_FILE_AVG
print ("Sorted output")
label_avg = '  j      timer_name             avg_total'
print(label_avg)
ttotal_avg, ttimer_name = (list(t) for t in zip(*sorted(zip(ttotal_avg, ttimer_name))))
for j in range(0,i):
    print("%3d   %s    %5.4f" % (j, ttimer_name[j], ttotal_avg[j]))

#----------------------------------------------------
# Plot data, Sorted
#----------------------------------------------------
# subplot 212
ax2.barh(timer_name_num[0:18],ttotal_avg[0:18],  height=0.4, align='center', color = colors)
ax2.set_yticks(timer_name_num)
ax2.set_yticklabels(ttimer_name[0:18])
ax2.set_xlabel('time')
ax2.set_ylabel('timer name')
ax2.set_title('Layer 5 - Sorted Ascending Order')
ax2.set_ylim((-1,18))
ax2.grid(True)

#----------------------------------------------------
# show the figure, but do not block
#----------------------------------------------------
plt.show()
fig.savefig('Unsorted_Sorted.png', bbox_inches='tight')
