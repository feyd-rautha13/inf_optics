# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import numpy as np
import matplotlib.pyplot as plt


filename = "D:\\work\\coding\\python\\OpticalTest\\code\\aoc.txt"

a = np.loadtxt(filename)
time = a[:,0]
time = [x-time[0] for x in time]

temp = a[:,1]


# Plot Y1
fig = plt.figure(figsize=(12,9))

ax1 = fig.add_subplot(111)
ax1.plot(time, temp, label='Temp')

ax1.set_title('Temperature vs BER for QSFP-DD AOC PRBS31Q')
ax1.set_xlabel('Time(s)')
ax1.set_ylabel('Temp(C)')
ax1.set_ylim([-5,80])
#ax1.legend()


## Plot Y2 
ax2 = ax1.twinx()

for i in range(2, a.shape[1]):
    ax2.semilogy(time, a[:,i], label = 'L{0}'.format(i-2))
    
ax2.hlines(2.4E-4, 0, 60000, colors = 'r', linestyles = 'dashed', label = 'Threshold')
ax2.set_ylabel('BER')
ax2.set_ylim([1E-12,1E-3])

# Legend
handles1, labels1 = ax1.get_legend_handles_labels()     
handles2, labels2 = ax2.get_legend_handles_labels()     
plt.legend(handles1+handles2, labels1+labels2)

plt.show()

