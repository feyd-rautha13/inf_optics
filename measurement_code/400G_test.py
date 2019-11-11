# /usr/bin/env python
# -*- coding : utf-8 -*-

'''
QSFP-DD DR4 test
'''

import sys

interface_path = "D:\\work\\coding\\python\\inf_optics\\interface"
component_path = "D:\\work\\coding\\python\\inf_optics\\Test\\component"
device_path = "D:\\work\\coding\\python\\inf_optics\\labdevice"
eeprom_path = "D:\\project\\pluggable\\400G\\400G EEPROM\\QSFP-DD EEPROM Spec-Mar25.xlsx"



sys.path.append(interface_path)
sys.path.append(component_path)
sys.path.append(device_path)


###############################################
from SSHinterface import groove_Hal
from transceiver import QSFPDD
from EXFO_LTB8 import LTB8

import numpy as np
import openpyxl
import threading


groove_ip = '172.29.150.194'
LTB_ip = "172.29.150.191"
LTB_port = 5025


hal = groove_Hal(host = groove_ip,port = 8022, 
                 username = 'administrator' , password = 'e2e!Net4u#',
                 timeout = 10, halusername = 'su', halpassword = 'cosh1$')

#box = LTB8(LTB_ip, LTB_port)


###############################################

#dr4 = QSFPDD(hal,1,8)
fr4 = QSFPDD(hal,1,7)


import time
from datetime import datetime

def track_temp(box):
    
    case = []
    tmp = str(round(dr4.ModMonCaseTemp,3))
    case = [tmp]
    for i in range(8):
        L0 = str(box.BERperLane(i))
        case.append(L0)
    return case

def logdata(name, data):
    with open('{0}.txt'.format(name),'a') as f:
        for i in data:
            f.writelines(i)
            f.writelines('\t')
        f.writelines('\n')
    
def logtime(name, time):
    with open('{0}.txt'.format(name), 'a') as f:
        f.writelines(time)
        f.writelines('\t')

    
def cycle_def(name):
#    init_time = datetime.now()
    box = LTB8(LTB_ip, LTB_port)
    time.sleep(2)
    
    box.ResetTest()
    time.sleep(12)
    
    current = str(time.time())
    
    logtime(name, time = current)
    logdata(name, data = track_temp(box))
    
    time.sleep(3)
    box.close()


def track(n, name):
    i = int(60*n)
    while(i>0):
        
        cycle_def(name)
        time.sleep(30)
        i -= 1

def toggleTx():
    dr4.ModDisableAllLaser
    time.sleep(0.15)
    dr4.ModEnableAllLaser
        
       
   
    
    
    
    
    
    
    
    
    
    
