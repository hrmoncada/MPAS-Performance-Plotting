"""
Version 2
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
import re
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

#----------------------------------------------------
# Chose plot type
#----------------------------------------------------
print('Plot Type:','  1: Network','  2: Testcase',sep='\n')
print(' ')
PlotType = int(
input("Please Enter the Plot-Type Integer: "))
print(' ') 

if PlotType == 1 : # Network file list
  print('Network:','  1: grizzly','  2: badger','  3: cori-haswell','  4: cori-knl',sep='\n')
  print(' ') 
  Network = int(input("Please Enter the Network Integer: "))
  Network_list = ['grizzly','badger','cori-haswell','cori-knl']
  print('\nNetwork : ',Network_list[Network-1])
  # Abort the execution
  sys.exit("aa! errors!")
elif PlotType == 2 : # Test case list
  print('TestCases:','  1: EC60to30','  2: RRS18to6','  3: RRS30to10',sep='\n')
  print(' ')
  TestCase = int(input("Please Enter the TestCase Integer: "))
  TestCase_list = ['EC60to30','RRS18to6','RRS30to10']
  print('\nTest case : ',TestCase_list[TestCase-1])
else :  
  print ,'Wrong !!! try again '
print(' ')   

#----------------------------------------------------
# Create the folders file list
#----------------------------------------------------
print('On Data:')
list_of_files = glob.glob('data/'+TestCase_list[TestCase-1]+'*')
filename = []
Network  = []
Case_name = []
# Print the files names request to be plot
for line in list_of_files:
    filename.append(line.split('/')[1])
    Case_name.append(re.split('[/ _ .]',line)[1])
    Network.append(re.split('[/ _ .]',line)[2])
    print(" %s "% line.split('/')[1])

print(' ') 
#print(filename)
#print(Network)
#print(Case_name)
#print('Chosen TestCase : ', )

# Open the data files with read only permit
data_path = cwd+'/'+'data'+'/'
data_1 = open(data_path+filename[0], 'r')
data_2 = open(data_path+filename[1], 'r')

#----------------------------------------------------
# Set empty arrays for grizzly
#----------------------------------------------------
Cores_G = []
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
plt.clf()
f = plt.figure(1) 
plt.subplot(121)
plt.loglog(Cores_G, SYPD_G,'ro-', linewidth=1, markeredgewidth= 0, markersize=10, label=Case_name[0]+', '+ Network[0])
plt.loglog(Cores_G, Perfect_Scaling_SYPD_G,'k*--', linewidth=2, markeredgewidth= 0, markersize=10, label='Perfect Scaling')
plt.loglog(Cores_B, SYPD_B,'bs-', linewidth=1, markeredgewidth= 0, markersize=5, label=Case_name[1]+', '+Network[1])

plt.xlabel('Number of MPI ranks', fontsize=14, weight='bold')
plt.ylabel('Simulated Years per Day (SYPD)', fontsize=14, weight='bold')
plt.title('MPAS-ocean Performance Curve', fontsize=14, weight='bold')
plt.tight_layout()
plt.grid(which='major')
plt.legend(loc='upper left')

#plt.figure(2) 
plt.subplot(122)
plt.plot(Cores_G, Performance_Time_G,'ro-', linewidth=1, markeredgewidth= 0, markersize=10, label= Case_name[0]+', '+ Network[0])
plt.plot(Cores_B, Performance_Time_B,'bs-', linewidth=1, markeredgewidth= 0, markersize=5, label=Case_name[0]+', '+ Network[0])
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
plt.show(block=False) # block=False, allow the code to continue into the next step
f.savefig(Case_name[0]+'_result.pdf', bbox_inches='tight')

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
