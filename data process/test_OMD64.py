# /usr/bin/env python
# -*- coding : utf-8 -*-

"""
Created on Tue Nov 13 10:31:44 2018
Modified on 
File description: Test data
    
"""

__author__ = 'Sizhan Liu'
__version__ = "1.0"


channel_plan_path = "C:\\Data\\sliu3\\Documents\\work\\coding\\python\\OpticalTest\\OMD64\\channelplan.csv"
demux_data_path = "C:\\Data\\sliu3\\Documents\\work\\coding\\python\\OpticalTest\\OMD64\\demux_data"
mux_data_path = "C:\\Data\\sliu3\\Documents\\work\\coding\\python\\OpticalTest\\OMD64\\mux_data"


from passive_data_process import *
import os
import numpy as np
import time

keywords = 'mux'

def channel_plan(path):
    '''
    Get channel plan from csv file. 
    coloum 0 = channel id
    coloum 1 = center frequency unit = Ghz
    coloum 2 = center wavelength unit = nm
    '''    
    channel_plan = np.loadtxt(path, delimiter = ',', usecols=(0,1,2))
    return channel_plan


def get_data_list(path = None, keywrods = None):
    '''
    Get data file name list 
    '''
    data_list = os.listdir(path)
    data_list = [x for x in data_list if keywords in x]
    return data_list

channel_plan = channel_plan(channel_plan_path)
data_name_list = get_data_list(demux_data_path)
channel_num = np.linspace(1,64,64, dtype=np.int0)

start = time.time()


print("chn\t","freq\t","wavelength\t","IL\t","db_5p\t","ccp_5\t",
      "db_1p\t","ccp_1\t","db_3p\t","ccp_3\t","freq_shift\t","il_ripple\t","pdl\t",
      "pmd\t","cd\t","gdr\t","adj\t","nadj\n")

for i in channel_num:
    chx = channel(i, data_name_list = data_name_list, channel_plan = channel_plan)
    parameter = chx.channel_parameter()
    chn = parameter[0]
    freq = parameter[1]
    wavelength = parameter[2]
    IL = parameter[3]
    
    
    db_5 = chx.passband(0.5)
    db_5p = db_5[2]
    ccp_5 = db_5[3]
    
    db_1 = chx.passband(1)
    db_1p = db_1[2]
    ccp_1 = db_1[3]
    
    db_3 = chx.passband(3)
    db_3p = db_3[2]
    ccp_3 = db_3[3]
    
    freq_shift = chx.freq_shift 
    il_ripple = chx.il_ripple
    pdl = chx.pdl
    pmd = chx.pmd
    
    gdr = chx.gdr_cd(freq_L=chx.freq_sp_L_val, freq_R=chx.freq_sp_R_val, order = 2)
    cd = gdr[0]
    gdr_1 = gdr[1]
    
    xtalk = chx.xtalk()
    adj = xtalk[0]
    nadj = xtalk[1]
    
    print(chn,freq,wavelength,IL,db_5p,ccp_5,db_1p,ccp_1,db_3p,ccp_3,freq_shift,il_ripple,pdl,pmd,cd,gdr_1,adj,nadj)
    
stop = time.time()
print (stop - start)  

