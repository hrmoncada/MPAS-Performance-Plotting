'''
python3 Henry_plot_log_pfiles_8.py  ' 5 '

Enter the number of cores = 16


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

#----------------------------------------------------
# Start time
#----------------------------------------------------
start_time = time.time()

#----------------------------------------------------
# Used to split the text part from the numbers
#----------------------------------------------------
def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

#-----------------------------------------------------------------------------
# "argv" represents all the items that come along via the command line input,
# Remember that sys.argv[0], item_0 = It is the  name of the script.
#-----------------------------------------------------------------------------
print ("This is the name of the script: %s\n"% sys.argv[0]) # program name

#----------------------------------------------------------------------------------------
#  sys.argv[1], item_1 = It is the "input key" to be search and found on the _INPUT_FILE
#----------------------------------------------------------------------------------------
pattern = re.compile('^(.*)' + re.escape(sys.argv[1]) + '(.*)$')

#----------------------------------------------------
# Get the current directory path
#----------------------------------------------------
cwd = os.getcwd()
print("Current path folder = %s\n"% cwd)

#----------------------------------------------------
# Netwrok 
#----------------------------------------------------
print('Network:','  1: LANL-Grizzly','  2: LANL-Badger','  3: NERSC-Cori Haswell','  4: NERSC-Cori KNL', '  5: ORNL-Summit',sep='\n')
print(' ')
Network = int(input("Please Enter the Network Integer: "))
Network_list = ['LANL_Grizzly/','LANL_Badger/','NERSC_Cori_Haswell/','NERSC_Cori_KNL/', 'ORNL_Summit/']
Net_keyword = Network_list[Network-1]
print(' ')
#----------------------------------------------------
# TestCase 
#----------------------------------------------------
print('TestCases:','  1: EC60to30','  2: RRS18to6','  3: RRS30to10',sep='\n')
print(' ')
TestCase = int(input("Please Enter the TestCase Integer: "))
TestCase_list = ['EC60to30/','RRS18to6/','RRS30to10/']
Test_keyword = TestCase_list[TestCase-1]

#----------------------------------------------------
# Create the list of folders and get the cores list
#----------------------------------------------------
list_of_folders = glob.glob('data/' + Net_keyword + Test_keyword + 'perf_p*_gr_openmpi')
#print("Print folders list :")
#for line in list_of_folders:
  #print(" %s "% line)
print("")

#----------------------------------------------------
# Sorted files in ascending cores number order
#----------------------------------------------------
cores = []                                   # array cores numbers
list_of_folders.sort(key   =  natural_keys)  # key = number

print("Sorted Folders list in ascending core-number order:")
for line in list_of_folders:
  print(" %s "% line)
  x = re.split('(\d+)',line)
  cores.append(x[1])
print('') 

#-------------------------------------------------------------------------
# Input the number of cores that belongmtpo the files you which to search
#------------------------------------------------------------------------
cores = input("Enter the number of cores = ")
print('')

#---------------------------------------------------
# Get the files folder-path
#----------------------------------------------------
folder = 'data/' + Net_keyword + Test_keyword + 'perf_p' + cores + '_gr_openmpi'
folder_path = cwd+'/'+folder+'/'

# Create the list of files
list_of_files = glob.glob('data/' + Net_keyword + Test_keyword + 'perf_p'+cores+'_gr_openmpi/log_p'+cores+'_s*')

# Print folder files
print("Files list: %s" % folder)
for line in list_of_files:
    print(" %s "% line)

#---------------------------------------------------------
# Open output file  "_OUTPUT_FILE" with write only permit
#---------------------------------------------------------
OutputNameFile = 'File_Output.txt'
_OUTPUT_FILE = open(cwd + '/' + OutputNameFile, 'w')

# Label line write in _OUTPUT_FILE
labels = 'Layer    timer_name                                        total       calls        min            max            avg      pct_tot   pct_par     par_eff    i'

# Write "labels" into _OUTPUT_FILE
_OUTPUT_FILE.write(labels + os.linesep)

#----------------------------------------------------
# Store array variables
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
# Split "perf_p16_gr_openmpi/log_p16_s = perf_p16_gr_openmpi + log_p16_s  = File[0] + File[1]"  
  File = file_name.split("/")
  print("Read filename  = ", File[1],"\n") # print filename
  
# file	name
  InputNameFile = File[4]

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
            # print(match)
             _OUTPUT_FILE.write(match.group() + os.linesep)# Save information
             name = match.group()                          #
             #print(match.group() + '      ' + str (i))    # Print all columns (0 to 8)
             name = name.strip(' ')                        # Split columns
             timer_name.append(name[6:31])                 # Store timer_name (col 1)
             total.append(name[55:62])                     # Store total (col 2)
             calls.append(name[70:73])                     # Store calls (col 3) = Number of times a funciton was called
             avg.append(name[110:117])                     # Store avg   (col 6) = Average time
             count.append(i)                               # Store variable index counter
             #print(name[6:31],name[55:62],name[70:73],name[110:117],len(name), i) # print the 3 files (s1,s2,s3) require variables 
             i+=1  # Variable label counter, increment 

# Close _OUTPUT_FILE
_OUTPUT_FILE.close()

print("\nNum Subroutines = %d"% i)
print ("\nUnsorted output : ")

# Open the OUTPUT file with write only permit
OutputNameFileAvg = 'File_Output_Avg.txt'
_OUTPUT_FILE_AVG = open(cwd +'/' + OutputNameFileAvg, 'w')

# Label line write in _OUTPUT_FILE_AVG
label_avg = '  j      timer_name             avg_total avg_calls  avg_avg'
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
# Set the colors
#----------------------------------------------------
#timer_name_num = list(range(0,i))
timer_name_num  = np.arange(len(ttimer_name))
colorcolor = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
#print(timer_name_num)
#print(len(ttimer_name), len(colors)) # (18, 7)
#print (range(0,len(colors)))  # [0, 1, 2, 3, 4, 5, 6]

m=0
n=0
colors = []
while  (n < len(ttimer_name)):         # <- while loop until reseach len(ttimer_name)
    for k in range(0,len(colorcolor)): # <- for loop
        n = m*len(colorcolor) + k
        colors.append(colorcolor[k])
        #print (m, i, n, colorcolor[i], colors[n])
        if not n <= len(ttimer_name):
            break                      # <- break the for loop
    m += 1
    
#----------------------------------------------------
# Plot data, Unsorted
#---------------------------------------------------- 
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
print ("\nSorted output : ")
label_avg = '  j      timer_name             avg_total   colors'
print(label_avg)
ttotal_avg, ttimer_name, colors = (list(t) for t in zip(*sorted(zip(ttotal_avg, ttimer_name, colors))))
#ttotal_avg, colors = (list(t) for t in zip(*sorted(zip(ttotal_avg, colors))))

for j in range(0,i):
    print("%3d   %s    %5.4f     %s" % (j, ttimer_name[j], ttotal_avg[j], colors[j]))

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
plt.show(block=False) # block=False, allow the code to continue into the next step
fig.savefig('Unsorted_Sorted.png', bbox_inches='tight')

#----------------------------------------------------
# Press any key to terminate
#----------------------------------------------------
#plt.pause(5)
while(True):
  print("Elapsed time: %6.4s seconds" % (time.time() - start_time))
  key = input("Press any key to terminate: ")
  if(len(key) >= 0):  
    plt.close()  # close figures
    break