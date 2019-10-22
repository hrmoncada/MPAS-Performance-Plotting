"""
Version 5
$ python3 HPC_cluster_system_performace.py 
Networks:
  1: grizzly
  2: badger
  3: cori-haswell
  4: cori-knl
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
import warnings;warnings.filterwarnings('ignore')

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
# Choose Plot Type 
#----------------------------------------------------
print('Plot Type:','  1: Network','  2: Testcase',sep='\n')
print(' ')
PlotType = int(input("Please Enter the Plot-Type Integer: "))
print(' ') 

#----------------------------------------------------
# Choose List Type 
#----------------------------------------------------
if PlotType == 1 : # Network file list
  print('Network:','  1: grizzly','  2: badger','  3: cori-haswell','  4: cori-knl',sep='\n')
  print(' ')
  Network = int(input("Please Enter the Network Integer: "))
  Network_list = ['grizzly','badger','cori-haswell','cori-knl']
  keyword = Network_list[Network-1]
elif PlotType == 2 : # Test case list
  print('TestCases:','  1: EC60to30','  2: RRS18to6','  3: RRS30to10',sep='\n')
  print(' ')
  TestCase = int(input("Please Enter the TestCase Integer: "))
  TestCase_list = ['EC60to30','RRS18to6','RRS30to10']
  keyword = TestCase_list[TestCase-1]
else :  
  print ,'Wrong !!! try again '
print(' ')   

#----------------------------------------------------
# Create the folders file list
#----------------------------------------------------
filename = []
Network  = []
Case_name = []

print('The plot contains the following information : ')  

if PlotType == 1 : # Search data/ for Network
  print('   Network : ',keyword)
  list_of_files = glob.glob('data/'+'*'+keyword+'*')
# Print the testcases files names request to be plot
  for line in list_of_files:
     filename.append(line.split('/')[1])
     Case_name.append(re.split('[/ _ .]',line)[1])
     Network.append(re.split('[/ _ .]',line)[2]) 
  print("   Test cases:", *Case_name, sep=', ')
elif PlotType == 2 : # Search data/ for Testcases
  print('  Test case : ',keyword)
  list_of_files = glob.glob('data/'+keyword+'*')
# Print the  network files names request to be plot
  for line in list_of_files:
     filename.append(line.split('/')[1])
     Case_name.append(re.split('[/ _ .]',line)[1])
     Network.append(re.split('[/ _ .]',line)[2])
  print("   Networks:", *Network, sep=', ')
else :  
  print ,'Wrong !!! try again '
print(' ') 
    
#----------------------------------------------------
# Open the data files with read only permit
#----------------------------------------------------
data_path = cwd+'/'+'data'+'/'

#----------------------------------------------------
# Color array
#----------------------------------------------------
colours=['b', 'g', 'r', 'c', 'm', 'y', 'k']

#----------------------------------------------------
# Initialize data plot 
#---------------------------------------------------- 
f = plt.figure() 

# Create an empty list, for 1D array (to be scale 2D array)
Cores = []
Performance_Time = []
Perfect_Scaling  = []
Perfect_Scaling_SYPD = []
SYPD = []

for i in range(len(filename)):   # i index the testcases
  data = open(data_path+filename[i], 'r')

# Create an empty list, inside a empty list, for a 2D array
  Cores.append([])
  Performance_Time.append([])
  SYPD.append([])

# Add elements to empty lists.
  n = 0
  for line in data:
     if (n > 6):  
       words = line.split()  
       Cores[i].append(int(words[0]))                # Number of Cores
       Performance_Time[i].append(float(words[4]))   # Average Time Performance
       SYPD[i].append(float(words[5]))               # SYPD - Simulated Years Per Wall Clock Day
# Check if line is not empty
     if not line:
       break
     n += 1

# Close the file after reading the lines.
  data.close()
  
# Plots Data LogLog
  f.add_subplot(121)
  plt.loglog(Cores[i], SYPD[i],'ro-', linewidth=1, markeredgewidth= 0, markersize=10, label=Case_name[i]+', '+ Network[i], color=colours[i])
# Plot data    
  f.add_subplot(122)
  plt.plot(Cores[i], Performance_Time[i],'ro-', linewidth=1, markeredgewidth= 0, markersize=10, label= Case_name[i]+', '+ Network[i], color=colours[i])
  
# Array size  
print("Arrays           (rows, cols)")
print("-------------------------------")
print("Cores            = (%d , %d)"%(len(Cores), len(Cores[0]))) #(rows, columns)
print("Performance_Time = (%d , %d)"%(len(Performance_Time), len(Performance_Time[0])))
print("SYPD             = (%d , %d)"%(len(SYPD),len(SYPD[0])))
#print(Cores)      
print("")
 
#----------------------------------------------------
# Plot Cosmetic Features - labes
#----------------------------------------------------  
#Plot loglog 
f.add_subplot(121)
plt.xlabel('Number of MPI ranks', fontsize=14, weight='bold')
plt.ylabel('Simulated Years per Day (SYPD)', fontsize=14, weight='bold')
plt.title('MPAS-ocean Performance Curve', fontsize=14, weight='bold')
plt.tight_layout()
plt.grid(which='major')
# Plot data
f.add_subplot(122)
plt.xlabel('Number of MPI ranks', fontsize=14, weight='bold')
plt.ylabel('Performance Time', fontsize=14, weight='bold')
plt.title('MPAS-ocean Performance Curve', fontsize=14, weight='bold')
plt.tight_layout()
plt.grid(which='major')
 
  
#----------------------------------------------------
# Show figure
#----------------------------------------------------
plt.show(block=False) # block=False, allow the code to continue into the next step

#----------------------------------------------------
# Perfect Scaling - Testcase file list
#----------------------------------------------------
if PlotType == 2 : 
# Reverse array function
  def reverse(L):
    L = [listElem[::-1] for listElem in L[::-1]]
    return L
    
  Cores = reverse(Cores)
  Performance_Time = reverse(Performance_Time)
  SYPD = reverse(SYPD)
  print("Perfect Scaling - Reverser  2D arrays\n")
  
# Array size  
  print("Arrays           (rows, cols)")
  print("-------------------------------")
  print("Cores            = (%d , %d)"%(len(Cores), len(Cores[0]))) #(rows, columns)
  print("Performance_Time = (%d , %d)"%(len(Performance_Time), len(Performance_Time[0])))
  print("SYPD             = (%d , %d)"%(len(SYPD),len(SYPD[0])))
  #print(Cores)
  print("")
  
# Pick point 
  Perf_length = len(SYPD[1])
  print("From the plot choose the best point")
  print("Range values are [0,%d]"%(len(SYPD[1])-1))
  print(' ')  
  plt.pause(0.001)
  #input("Press [enter] to continue.") 
# Best point    
  pick_point = int(input("Type best point to draw the perfect plot : "))
  print(' ')
  print("| Num | Cores | Performance_Time | Perfect_Scaling | Perfect_Scaling_SYPD |")
  print('----------------------------------------------------------------------------')
  for num in range(0,Perf_length):
    if num <= pick_point :
      Perfect_Scaling.append(Performance_Time[1][pick_point]*(2**(pick_point-num)))
      Perfect_Scaling_SYPD.append(SYPD[1][pick_point]/(2**(pick_point-num)))
      print("  %2d    %3d       %5.3f             %5.3f             %5.3f "%(num, Cores[1][num], Performance_Time[1][num], Perfect_Scaling[num] , Perfect_Scaling_SYPD[num]))
    elif num > pick_point : 
      Perfect_Scaling.append(Performance_Time[1][pick_point]/(2**(num-pick_point)))
      Perfect_Scaling_SYPD.append((2**(num-pick_point))*SYPD[1][pick_point])
      print("  %2d    %3d       %5.3f             %5.3f             %5.3f "%(num, Cores[1][num], Performance_Time[1][num], Perfect_Scaling[num] , Perfect_Scaling_SYPD[num]))
    else :  
     print('Wrong !!! try again ')
     
# Plot Perfect Scaling arrays loglog
  f.add_subplot(121)
  plt.loglog(Cores[1], Perfect_Scaling_SYPD,'k*--', linewidth=2, markeredgewidth= 0, markersize=10, label='Perfect Scaling')
# Plot data  
  f.add_subplot(122)
  plt.plot(Cores[1], Perfect_Scaling,'k*--', linewidth=2, markeredgewidth= 0, markersize=10, label= 'Perfect Scaling')

#----------------------------------------------------
# Plot Cosmetic Features - Legend
#----------------------------------------------------  
#Plot loglog 
f.add_subplot(121)
#plt.legend(loc='upper left')
plt.legend(loc='upper left',fontsize='medium')
# Plot data
f.add_subplot(122)
plt.xlim(xmin=-20)
plt.ylim(ymin=-20) # Set 'auto' for upper limit, but keep a fixed lower limit 
#plt.xlim(-20,(Cores[1][-1]+50))
#plt.ylim(-10,(Performance_Time[1][0]+100))
#plt.autoscale(tight=True)
#plt.autoscale(enable=True, axis='y')
#plt.legend(loc='upper left')
plt.legend(loc='upper right', fontsize='medium')  
  
#----------------------------------------------------
# Show figure
#----------------------------------------------------
plt.show(block=False) # block=False, allow the code to continue into the next step
#----------------------------------------------------
# Save figure
#----------------------------------------------------
f.savefig(Case_name[0]+'_result.pdf', bbox_inches='tight')

#----------------------------------------------------
# Press any key to terminate
#----------------------------------------------------
#plt.pause(5)
print(' ')  
while(True):
  print("Elapsed time: %6.4s seconds" % (time.time() - start_time))
  key = input("Press any key to terminate: ")
  if(len(key) >= 0):  
    plt.close()  # close figures
    break
