"""
Version 4
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
# Chose Plot Type
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
list_of_files = glob.glob('data/'+TestCase_list[TestCase-1]+'*')
filename = []
Network  = []
Case_name = []
# Print the files names request to be plot
for line in list_of_files:
    filename.append(line.split('/')[1])
    Case_name.append(re.split('[/ _ .]',line)[1])
    Network.append(re.split('[/ _ .]',line)[2])
   

print("Networks:")
#print(*Network, sep='\n')
print(*Network, sep=', ')
print(' ') 
#----------------------------------------------------
# Open the data files with read only permit
#----------------------------------------------------
data_path = cwd+'/'+'data'+'/'

#----------------------------------------------------
# Color array
#----------------------------------------------------
colours=['r','g','b','k']

#----------------------------------------------------
# Initialize data plot 
#---------------------------------------------------- 
# Create plottting 
#plt.clf()
f = plt.figure() 
#----------------------------------------------------
# Create an empty list, for 1D  array
#----------------------------------------------------
Cores = []
Performance_Time = []
Perfect_Scaling  = []
Perfect_Scaling_SYPD = []
SYPD = []

for i in range(len(filename)):  
  data = open(data_path+filename[i], 'r')
  #print(data.read())
#----------------------------------------------------
# Create an empty list, inside a empty list, for a 2D array
#----------------------------------------------------
  Cores.append([])
  Performance_Time.append([])
  SYPD.append([])
#----------------------------------------------------
# Add elements to empty lists.
#----------------------------------------------------
  n = 0
  for line in data:
     if (n > 6):  
       words = line.split()  
       Cores[i].append(int(words[0]))                # Number of Cores
       Performance_Time[i].append(float(words[4]))   # Average Time Performance
       SYPD[i].append(float(words[5]))               # SYPD
# check if line is not empty
     if not line:
       break
     n += 1

# close the file after reading the lines.
  data.close()
  
# Plots Data
  f.add_subplot(121)
  plt.loglog(Cores[i], SYPD[i],'ro-', linewidth=1, markeredgewidth= 0, markersize=10, label=Case_name[i]+', '+ Network[i], color=colours[i])
  
  f.add_subplot(122)
  plt.plot(Cores[i], Performance_Time[i],'ro-', linewidth=1, markeredgewidth= 0, markersize=10, label= Case_name[i]+', '+ Network[i], color=colours[i])

#----------------------------------------------------
# Reverse array function
#----------------------------------------------------
def reverse(L):
	L = [listElem[::-1] for listElem in L[::-1]]
	return L
Cores = reverse(Cores)
Performance_Time = reverse(Performance_Time)
SYPD = reverse(SYPD)

#----------------------------------------------------
# Perfect Scaling
#----------------------------------------------------
Perf_length = len(SYPD[0])
for num in range(0,Perf_length): 
     Perfect_Scaling.append(Performance_Time[0][0]/(2**num))
     Perfect_Scaling_SYPD.append((2**num)*SYPD[0][0])

#----------------------------------------------------
# Plot Perfect Scaling
#----------------------------------------------------
f.add_subplot(121)
plt.loglog(Cores[0], Perfect_Scaling_SYPD,'k*--', linewidth=2, markeredgewidth= 0, markersize=10, label='Perfect Scaling')
plt.xlabel('Number of MPI ranks', fontsize=14, weight='bold')
plt.ylabel('Simulated Years per Day (SYPD)', fontsize=14, weight='bold')
plt.title('MPAS-ocean Performance Curve', fontsize=14, weight='bold')
plt.autoscale(tight=True)
#plt.autoscale(enable=True, axis='y')
plt.tight_layout()
plt.grid(which='major')
plt.legend(loc='upper left')

f.add_subplot(122)
plt.plot(Cores[0], Perfect_Scaling,'k*--', linewidth=2, markeredgewidth= 0, markersize=10, label= 'Perfect Scaling')
#plt.xlim(-100,4200)
#plt.ylim(-10,600)
plt.autoscale(tight=True)
#plt.autoscale(enable=True, axis='y')
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
