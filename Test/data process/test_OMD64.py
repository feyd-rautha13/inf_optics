# /usr/bin/env python
# -*- coding : utf-8 -*-

"""
Created on Tue Nov 13 10:31:44 2018
Modified on 
File description: Test data
    
"""

__author__ = 'Sizhan Liu'
__version__ = "1.0"


import sys
import os
import numpy as np
import time
import pylab as pl

component_path = "D:\\work\\coding\\python\\inf_optics\\Test\\component"
test_data_path = 'D:\\project\\2018-07-09 OMD64\\2019-01-17 P1\\P1 convert\\mux\\'
channel_plan_path = 'D:\\project\\2018-07-09 OMD64\\2019-01-17 P1\\P1 convert\\channelplan.csv'
#test_data_path = 'D:\\project\\2018-07-09 OMD64\\2019-01-17 P1\\P1 convert\\demux\\'

sys.path.append(component_path)
from AWG import AWG

def get_data_real_path(path=None):
    name_list = os.listdir(path)
    data_real_path_list = [path + x for x in name_list]
    return data_real_path_list 

def channel_plan(path):
    '''
    Get channel plan from csv file. 
    coloum 0 = channel id
    coloum 1 = center frequency unit = Ghz
    coloum 2 = center wavelength unit = nm
    '''    
    channel_plan = np.loadtxt(path, delimiter = ',', usecols=(0,1,2))
    return channel_plan      

channel_plan = channel_plan(channel_plan_path) 
data_name_list = get_data_real_path(test_data_path)
channel_num = np.linspace(1,64,64, dtype=np.int0)

start = time.time()

'''



print("chn\t","freq\t","wavelength\t",
      "IL_cen\t","IL_best\t","IL_worst\t","IL_ripple\t",
      "db_5p\t","ccp_5\t",
      "db_1p\t","ccp_1\t",
      "db_3p\t","ccp_3\t",    
      "freq_shift\t",
      "pdl\t","pmd\t","cd\t","gdr\t",
      "adj\t","nadj\n")

for i in channel_num:
    chx = AWG(i, data_name_list = data_name_list, channel_plan = channel_plan)
    parameter = chx.channel_parameter()
    
    chn = parameter[0]
    freq = parameter[1]
    wavelength = parameter[2]
    
    IL = chx.IL()
    IL_cen = IL[0]
    IL_best = IL[1]
    IL_worst = IL[2]
    IL_ripple = IL[3]
    
    db_5 = chx.passband(0.5)
    db_5p = db_5[2]
    ccp_5 = db_5[3]
    
    db_1 = chx.passband(1)
    db_1p = db_1[2]
    ccp_1 = db_1[3]
    
    db_3 = chx.passband(3)
    db_3p = db_3[2]
    ccp_3 = db_3[3]
    
    freq_shift = db_3[4]

    pdl = chx.pdl
    pmd = chx.pmd
    
    gdr = chx.gdr_cd(2)
    cd = gdr[0]
    gdr_1 = gdr[1]
    
    xtalk = chx.xtalk()
    adj = xtalk[0]
    nadj = xtalk[1]
    
    print(chn,freq,wavelength,
          IL_cen,IL_best,IL_worst,IL_ripple,
          db_5p,ccp_5,
          db_1p,ccp_1,
          db_3p,ccp_3,
          freq_shift,
          pdl,pmd,cd,gdr_1,
          adj,nadj)
    
stop = time.time()
print (stop - start)  






'''



'''

ch32 = AWG(32, data_name_list = data_name_list, channel_plan = channel_plan)

spl = ch33.data_freq_sp_L_idx
spr = ch33.data_freq_sp_R_idx
x0 = ch33.data_wavelength[spl:spr]
y0 = ch33.data_Max_Loss[spl:spr]
y1 = ch33.data_Min_Loss[spl:spr]


pl.plot(x0,y0,label='Max Loss'), pl.plot(x0,y1, label='Min Loss'), pl.legend(),pl.show()

ch32.data_freq_sp_L_val
193718.957
ch32.data_freq_sp_R
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'AWG' object has no attribute 'data_freq_sp_R'
ch32.data_freq_sp_R_val
193656.08

'''