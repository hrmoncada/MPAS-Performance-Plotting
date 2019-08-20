import matplotlib.pyplot as plt
import os
import subprocess
import re

# file	name
filename = 'log_p16_s1'

# Open the file with read only permit
dataFile = open(filename, 'r')

# Read and print file
message = dataFile.read()
print(message)


# The variable "line" is a list containing all lines in the file
line = dataFile.readlines()
while line:
    # in python 2+
    # print line
    # in python 3 print is a builtin function, so
    #print(line)
    # use realine() to read next line
    line = f.readline()

dataFile.close()


'''
with dataFile as f:
    for line in f:
        line = line.rstrip() # remove trailing whitespace such as '\n'
        subprocess.call(['/bin/grep', line, 'log_p16_s1'])

'''

'''
# Search for �me integra�on and write to a file
for i in range(1,4): # loop over 1,2,3
  fr = open(filename, 'r')
  for line in fr:
    m = re.search("2 time integration", line)
    if m:
      numbers = line.split("integration", 1)[1]
      first_number = numbers.split()[0]
      #fw.write('%s \t' % first_number)
      sum = sum + float(first_number)
  fr.close()
 # fname = "log_p" + str(i) + "_s" + str(sample + 1)  #  log_p16_s1
  #filepath = foldername + "/" + fname
  #subprocess.check_call(['mv', filename, filepath])


'''

'''# Set arrays
Cores = []
Performance = []
Perfect_Scaling = []

n = 0
# Loop through each line of the input data file
for line in dataFile:
    if (n > 6):  
       words = line.split()  
       #print line # in python 2
       #print(i, line)  # in python 3
       Cores.append(int(words[0]))
       Performance.append(float(words[5]))
       
# check if line is not empty
    if not line:
        break
    n += 1

# close the file after reading the lines.
dataFile.close()

# Perfect Scaling
Perf_length = len(Performance)
for num in range(0,Perf_length): 
    Perfect_Scaling.append((2**num)*Performance[Perf_length-1])
# reverse Perfect Scaling array
Perfect_Scaling.reverse()   

# Plotting
plt.loglog(Cores, Performance,'ro-', linewidth=1, markeredgewidth= 0, markersize=10, label='EC60to30, grizzly')
plt.loglog(Cores, Perfect_Scaling,'k--', linewidth=2, label='Perfect Scaling')
plt.xlabel('Number of MPI ranks', fontsize=14, weight='bold')
plt.ylabel('Simulated Years per Day (SYPD)', fontsize=14, weight='bold')
plt.title('MPAS-ocean Performance Curve', fontsize=14, weight='bold')
plt.tight_layout()
plt.grid()
plt.legend(loc='upper left')
plt.show()
plt.savefig('result.png')

'''
