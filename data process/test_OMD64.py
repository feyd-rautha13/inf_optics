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
class_path = "C:\\Data\\sliu3\\Documents\\work\\coding\\python\\inf_optics\\data process"
channel_plan_path = "C:\\Data\\sliu3\\Documents\\work\\coding\\python\\OpticalTest\\OMD64\\channelplan.csv"
demux_data_path = "C:\\Data\\sliu3\\Documents\\work\\coding\\python\\OpticalTest\\OMD64\\demux_data"
mux_data_path = "C:\\Data\\sliu3\\Documents\\work\\coding\\python\\OpticalTest\\OMD64\\mux_data"

sys.path.append(class_path)
sys.path.append(channel_plan_path)
sys.path.append(demux_data_path)
sys.path.append(mux_data_path)


from passive_data_process import *
import os
import numpy as np
import pylab as pl
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
data_name_list = get_data_list(mux_data_path)
channel_num = np.linspace(1,64,64, dtype=np.int0)

#start = time.time()


#print("chn","freq","wavelength","db_5p","ccp_5","db_1p","ccp_1,db_3p","ccp_3",
#      "freq_shift","il_ripple","pdl","pmd","adj","nadj")

#for i in channel_num:
#    chx = channel(i)
#    parameter = chx.channel_parameter()
#    chn = parameter[0]
#    freq = parameter[1]
#    wavelength = parameter[2]
#    IL = parameter[3]
#    print (IL)
    
#    db_5 = chx.passband(0.5)
#    db_5p = db_5[2]
#    ccp_5 = db_5[3]
#    
#    db_1 = chx.passband(1)
#    db_1p = db_1[2]
#    ccp_1 = db_1[3]
#    
#    db_3 = chx.passband(3)
#    db_3p = db_3[2]
#    ccp_3 = db_3[3]
#    
#    freq_shift = chx.freq_shift 
#    il_ripple = chx.il_ripple
#    pdl = chx.pdl
#    pmd = chx.pmd
#    xtalk = chx.xtalk()
#    
#    adj = xtalk[0]
#    nadj = xtalk[1]
    
#    print(chn,freq,wavelength,db_5p,ccp_5,db_1p,ccp_1,db_3p,ccp_3,freq_shift,il_ripple,pdl,pmd,adj,nadj)
    
#stop = time.time()
#print (stop - start)  

