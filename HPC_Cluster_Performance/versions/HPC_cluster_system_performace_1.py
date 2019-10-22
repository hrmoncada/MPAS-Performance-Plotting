"""
Version 1
$ python3 HPC_cluster_system_performace.py 
TestCases:
  1: EC60to30
  2: RRS18to6
  3: RRS30to10
Please Enter the TestCase Integer: 1
You chose the TestCase :  EC60to30
"""

import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import glob
import time
#----------------------------------------------------
# Start time
#----------------------------------------------------
start_time = time.time()

#----------------------------------------------------
# Get the current directory path
#----------------------------------------------------
cwd = os.getcwd()
print("Current path folder = %s\n"% cwd)

#-----------------------------------------------------------------------------
# "argv" represents all the items that come along via the command line input,
# Remember that sys.argv[0], item_0 = It is the  name of the script.
#-----------------------------------------------------------------------------
print ("This is the name of the script: %s\n"% sys.argv[0])

print('TestCases:','  1: EC60to30','  2: RRS18to6','  3: RRS30to10',sep='\n')
TestCase = int(input("Please Enter the TestCase Integer: "))

# Pick one filename
if TestCase == 1:                     
   filename_1 = 'EC60to30_grizzly.txt'
   filename_2 = 'EC60to30_badger.txt'
elif TestCase == 2:  
  filename_1 = 'RRS18to6_grizzly.txt'
  filename_2 = 'RRS18to6_badger.txt'
elif TestCase == 3:     
  filename_1 = 'RRS30to10_grizzly.txt'
  filename_2 = 'RRS30to10_badger.txt'
else :
  print ,'Wrong !!! try again '
print(' ')  

# Slip folder name: 
parts_filename_1 = filename_1.split('_')
parts_filename_2 = filename_2.split('_')
#print line # in python 2
#print(i, line)  # in python 3
print('Chosen TestCase : ', parts_filename_1[0])
print ('Network : ', parts_filename_1[1])

# Open the data files with read only permit
data_path = cwd+'/'+'data'+'/'
data_1 = open(data_path+filename_1, 'r')
data_2 = open(data_path+filename_2, 'r')


#----------------------------------------------------
# Create the list of files with the parts_filename_1[0] name
list_of_files = glob.glob('data/'+parts_filename_1[0]+'*')

# Print the files names request to be plot
for line in list_of_files:
    print(" %s "% line)
print(' ') 
#----------------------------------------------------
# Set empty arrays for grizzly
#----------------------------------------------------
Cores_G= []
Performance_Time_G = []
Perfect_Scaling_G = []
Perfect_Scaling_SYPD_G = []
SYPD_G = []
#----------------------------------------------------
# Set empty arrays for badger
#----------------------------------------------------
Cores_B= []
Performance_Time_B = []
Perfect_Scaling_SYPD_B = []
SYPD_B = []
n = 0
#----------------------------------------------------
# Loop through each line of the input data file
#----------------------------------------------------
for line in data_1:
    if (n > 6):  
       words = line.split()  
       Cores_G.append(int(words[0]))                # Number of Cores
       Performance_Time_G.append(float(words[4]))   # Average Time Performance
       SYPD_G.append(float(words[5]))               # SYPD
# check if line is not empty
    if not line:
        break
    n += 1

# close the file after reading the lines.
data_1.close()

#print (*Cores_G,sep='\n')
#print (*Performance_Time_G,sep='\n')
#print (*SYPD_G,sep='\n')
#DATA = []
#DATA = np.c_[Cores_G, Performance_Time_G, SYPD_G]  # add columns
#print (*DATA,sep='\n')
#----------------------------------------------------
# Reverse array for Grizzly
#----------------------------------------------------
Cores_G.reverse()
Performance_Time_G.reverse()
SYPD_G.reverse() 

# Perfect Scaling
Perf_length_G = len(SYPD_G)
for num in range(0,Perf_length_G): 
    Perfect_Scaling_G.append(Performance_Time_G[0]/(2**num))
    Perfect_Scaling_SYPD_G.append((2**num)*SYPD_G[0])

'''# Best curve fit
z_SYPD = np.polyfit(Cores_G, SYPD_G,2)
z_Performance = np.polyfit(Cores_G, Performance_Time_G,2)

f_SYPD = np.poly1d(z_SYPD)
f_Performance = np.poly1d(z_Performance)

# calculate new x's and y's
#x_new = np.linspace(Cores_G[0], Cores_G[-1], 10)
y_SYPD = f_SYPD(Cores_G)
y_Performance = f_Performance(Cores_G)
'''
n = 0
# Loop through each line of the input data file
for line in data_2:
    if (n > 6):  
       words = line.split()  
       Cores_B.append(int(words[0]))
       Performance_Time_B.append(float(words[4]))
       SYPD_B.append(float(words[5]))
# check if line is not empty
    if not line:
        break
    n += 1

# close the file after reading the lines.
data_2.close()
#----------------------------------------------------
# Reverse array for Badger
#----------------------------------------------------
Cores_B.reverse()
Performance_Time_B.reverse()
SYPD_B.reverse() 

#----------------------------------------------------
# Plot data
#---------------------------------------------------- 
# Create plottting 
plt.clf()
f = plt.figure(1) 
plt.subplot(121)
plt.loglog(Cores_G, SYPD_G,'ro-', linewidth=1, markeredgewidth= 0, markersize=10, label=parts_filename_1[0]+', '+parts_filename_1[1])
plt.loglog(Cores_G, Perfect_Scaling_SYPD_G,'k*--', linewidth=2, markeredgewidth= 0, markersize=10, label='Perfect Scaling')
#plt.loglog(Cores_G, y_SYPD,'g*--', linewidth=2, markeredgewidth= 0, markersize=10, label='Perfect Scaling')
plt.loglog(Cores_B, SYPD_B,'bs-', linewidth=1, markeredgewidth= 0, markersize=5, label=parts_filename_2[0]+', '+parts_filename_2[1])
#plt.loglog(Cores_B, Perfect_Scaling_B,'m--', linewidth=2, label='Perfect Scaling')

plt.xlabel('Number of MPI ranks', fontsize=14, weight='bold')
plt.ylabel('Simulated Years per Day (SYPD)', fontsize=14, weight='bold')
plt.title('MPAS-ocean Performance Curve', fontsize=14, weight='bold')
plt.tight_layout()
plt.grid(which='major')
plt.legend(loc='upper left')

#plt.figure(2) 
plt.subplot(122)
plt.plot(Cores_G, Performance_Time_G,'ro-', linewidth=1, markeredgewidth= 0, markersize=10, label=parts_filename_1[0]+', '+parts_filename_1[1])
plt.plot(Cores_G, Perfect_Scaling_G,'k*--', linewidth=2, markeredgewidth= 0, markersize=10, label='Perfect Scaling')
#plt.plot(Cores_G, y_Performance,'g*--', linewidth=2, markeredgewidth= 0, markersize=10, label='Perfect Scaling')
plt.plot(Cores_B, Performance_Time_B,'bs-', linewidth=1, markeredgewidth= 0, markersize=5, label=parts_filename_2[0]+', '+parts_filename_2[1])
#plt.loglog(Cores_B, Perfect_Scaling_B,'m--', linewidth=2, label='Perfect Scaling')
plt.xlim(-100,4200)
plt.ylim(-10,600)
plt.xlabel('Number of MPI ranks', fontsize=14, weight='bold')
plt.ylabel('Performance Time', fontsize=14, weight='bold')
plt.title('MPAS-ocean Performance Curve', fontsize=14, weight='bold')
plt.tight_layout()
plt.grid(which='major')
plt.legend(loc='upper right')

#----------------------------------------------------
# Show and Save figure
#----------------------------------------------------
# plt.show()
plt.show(block=False) # block=False, allow the code to continue into the next step
# Save figure
f.savefig(parts_filename_1[0]+'_result.pdf', bbox_inches='tight')

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
