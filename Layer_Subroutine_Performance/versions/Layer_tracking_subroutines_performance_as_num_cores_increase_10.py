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
print ("This is the name of the script: %s\n"% sys.argv[0])

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
# Output folder name
#----------------------------------------------------
OutputNameFile = 'Performance_Output.csv'

#----------------------------------------------------
# Create the list of folders and get the cores list
#----------------------------------------------------
list_of_folders = glob.glob('perf_p*_gr_openmpi')
print("Read the Folders list :")
for line in list_of_folders:
  print(" %s "% line)
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

#----------------------------------------------------
# Loop over the folder list 
#----------------------------------------------------
k = 0 # count cores array
t_avg = [] # array to ttime avg by core numbers

for folder in list_of_folders:
# Get the folder-path   
  files_path  = folder +'/'+'log_p*'
  #print("%s\n"%files_path)

# Create the list of files in the folder
  list_of_files = glob.glob(files_path)#'perf_p16_gr_openmpi/log_p16_s*')
  #print("Files list: %s" % folder)
   
#----------------------------------------------------
# Store time variables
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
  for files in list_of_files:
  
# file name
     InputNameFile = cwd + '/'+ files  #File[1]

# Open the file with read only permit
     _INPUT_FILE = open(InputNameFile, 'r')

# Variable label counter , update  
     i = 0  
#---------------------------------------------------- 
# Search pattern on a files 
#----------------------------------------------------
     with _INPUT_FILE  as f:
         for line in f:
             match = pattern.match(line)
             if match is not None:
                #_OUTPUT_FILE.write(match.group() + os.linesep)# Save information
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
     #print("%3d   %s    %5.3f    %5.1f     %5.3f" % (j, ttimer_name[j], ttotal_avg[j], tcalls_avg[j], tavg_avg[j]))
     #_OUTPUT_FILE_AVG.write("%3d   %s    %5.3f    %5.1f     %5.3f\n" % (j, ttimer_name[j], ttotal_avg[j], tcalls_avg[j], tavg_avg[j]))

#----------------------------------------------------
# Print Subroutines total times by cores number
#----------------------------------------------------  
  print("(k,  cores) = (%d %s)"%(k, cores[k]))
  label_avg = 'j      timer_name             avg_total'
  print(label_avg)
  for mm in range(0,len(ttotal_avg)):
     print('%d  %s  %5.4f' %(mm, timer_name[mm],ttotal_avg[mm]))
  print("")
  t_avg = np.hstack((t_avg, ttotal_avg))
  k += 1
  
#-------------------------------------------------------------------------------------------
# Search Patttern End
#-------------------------------------------------------------------------------------------  

#-----------------------------------------------------------------------------------
# Extract the text name from the empty part on each line from the ttimer_name array
#----------------------------------------------------------------------------------
name = []  # new array to reshape the size on each line on ttime_name
for linename in ttimer_name:
    linename = linename.strip(' ')  # Split ttime_name 
    name.append(linename)
    #print(linename,len(linename))
#print('')

#--------------------------------------------------------------
# Reshape column array in 2d array - total_time by cores number
#--------------------------------------------------------------
print('Total time 1D array shape  ->    length = %d '%np.shape(t_avg))
print('')
t_avg = np.reshape(t_avg,(len(cores),-1))  # Reshape (216,1) 1D array to 2D array with 12 rows, (12,18) = (row,col)
#t_avg = np.reshape(t_avg,(-1,18)) # Reshape (216,1) 1D array to 2D array with 18 columns (12,18) = (row, col)
#print(t_avg)
#print('')
print('Total time 2D array reshape ->  (row col)= (%d, %d) '%np.shape(t_avg))
print('')

#----------------------------------------------------------------------
# Convert the 2D array into DataFrame with columns names = ttimer_name
#----------------------------------------------------------------------
df = pd.DataFrame(t_avg,columns=name)
#print(df)
#print(' ')
print('Dataframe shape ->  (row col) = (%d, %d) '%np.shape(df))
print(' ')

#--------------------------------------------------------------
# Insert Cores Number column into the dataframe
#--------------------------------------------------------------
idx = 0               # column number
new_col = cores       # can be a list, a Series, an array or a scalar   
df.insert(loc=idx, column='Cores', value=new_col)
print('Insert `Cores` column into the dataframe')
#print(df)
print(' ')

#--------------------------------------------------------------
# Set the index to become the ‘Cores’ column:
#--------------------------------------------------------------
df2 = df.set_index('Cores')
print('Set the index to become the`Cores` column:')
print(' ')

pd.set_option('colheader_justify', 'left')
print('Display dataframe\n')
print(df2)
print(' ')

print('dataframe ->  (row col) = (%d, %d) '%np.shape(df2))
print('')

#----------------------------------------------------
#Exporting and Saving Pandas DataFrames into a cvs file
#----------------------------------------------------
# Plain dataframe
df2.to_csv(cwd  + '/' + OutputNameFile, index=False, encoding='utf8')

# Without the Subroutine name and number of cores
#df2.to_csv(cwd  + '/' + OutputNameFile , header=False,  index=False) 

#----------------------------------------------------
# Plot data
#---------------------------------------------------- 
#plt.figure(); 

df3 = df2[df2.columns[0:6]]
df4 = df2[df2.columns[7:12]]
df5 = df2[df2.columns[13:18]]

axes2 = df2.plot.line()
plt.title('Layer Performance')
plt.xlabel('core number')
plt.ylabel('Time')
plt.grid()

axes3 = df3.plot.line()
plt.title('Layer Performance')
plt.xlabel('core number')
plt.ylabel('Time')
plt.grid()

axes4 = df4.plot.line()
plt.title('Layer Performance')
plt.xlabel('core number')
plt.ylabel('Time')
plt.grid()

axes5 = df5.plot.line()
plt.title('Layer Performance')
plt.xlabel('core number')
plt.ylabel('Time')
plt.grid()

# multiple subplots
#axes2 = df2.plot.line(subplots=True)
#type(axes2)

#----------------------------------------------------
# Show and Save figure
#----------------------------------------------------
#plt.show()
plt.show(block=False) # block=False, allow the code to continue into the next step

axes2.get_figure().savefig('Subroutine_performance1.png', bbox_inches='tight')
axes3.get_figure().savefig('Subroutine_performance2.png', bbox_inches='tight')
axes4.get_figure().savefig('Subroutine_performance3.png', bbox_inches='tight')
axes5.get_figure().savefig('Subroutine_performance4.png', bbox_inches='tight')

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



