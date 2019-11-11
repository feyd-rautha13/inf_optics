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
#add component class
component_path = "D:\\work\\coding\\python\\inf_optics\\Test\\component"
#add channel plan
channel_plan_path = 'D:\\work\\coding\\python\\OpticalTest\\code\\NEL_Sample_OMD64_channelplan.csv'
#add data path
mux_data_path = "D:\\project\\passive\\2018-07-09 OMD64\\6-26 NEL OMD\\pure data\\mux\\"

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
data_name_list = get_data_real_path(mux_data_path)
channel_num = np.linspace(1,70,70, dtype=np.int0)





'''

start = time.time()
print("chn\t","freq\t","wavelength\t",
      "IL_cen\t","IL_best\t","IL_worst\t","IL_ripple\t",
      "db_5p\t","ccp_5\t",
      "db_1p\t","ccp_1\t",
      "db_3p\t","ccp_3\t",    
      "freq_shift\t",
      "pdl\t","pmd\t","cd\t","gdr\t",
      "adj\t","nadj\n")


for i in channel_num[3:]:
    chx = AWG(i, sp = 27.5, data_name_list = data_name_list, channel_plan = channel_plan, indexoffset=3)
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
    
    xtalk = chx.xtalk(first_chn = 4, last_chn = 70, passband = 9)
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