# /usr/bin/env python
# -*- coding : utf-8 -*-

'''
QSFP28 I2C test, all device

'''

#----- Add lib path ------
interface_path = "D:\\work\\coding\\python\\inf_bitbucket\\infinera_instrument_drivers\\interface"
component_path = "D:\\work\\coding\\python\\inf_bitbucket\\infinera_instrument_drivers\\Test\\component"
device_path = "D:\\work\\coding\\python\\inf_bitbucket\\infinera_instrument_drivers\\labdevice"


import sys
sys.path.append(interface_path)
sys.path.append(component_path)
sys.path.append(device_path)


#----- import user defined lib --------
from SSHinterface import groove_Hal
from SSHinterface import groove_cli
from transceiver import QSFP28


# ------ import 3rd part lib ------------
import time

# -- declare vars ----------------
groove_ip = '172.29.150.194'


# ------ class instance ------
hal = groove_Hal(host = groove_ip,port = 8022, 
                 username = 'administrator' , password = 'e2e!Net4u#',
                 timeout = 10, halusername = 'su', halpassword = 'cosh1$')

cli = groove_cli(host = groove_ip, port = 8022, username = 'administrator', 
                 password = 'e2e!Net4u#')


q1 = QSFP28(hal,1,6)
q2 = QSFP28(hal,1,7)
q3 = QSFP28(hal,1,8)

#partnumber = ['FTLC1154SDPL-S1 ', '1002971201      ', '1002971201      ']
partnumber = ['FTLC1154SDPL-S1 ','TR-IQ13L-NCT    ' , 'TR-IQ13L-NCT    ']

# -- define temp test function --
def get_data(dev):
    raw_data = dev.reg_get(0,168,16)
    pn = [chr(int(x,16)) for x in raw_data]
    s=''
    ss=''
    for i in raw_data:
        s += i
    for i in pn:
        ss += i
    result = str(ss in partnumber)
    
    return s,ss,result
 
    

def logdata(name, data):
    with open('{0}.txt'.format(name),'a') as f:
        for i in data:
            f.writelines(i)
            f.writelines('\t')
    

def test(filename, sleeptime):

    logdata(filename, get_data(q1))
    time.sleep(sleeptime)
    logdata(filename,get_data(q2))
    time.sleep(sleeptime)
    logdata(filename,get_data(q3))
    time.sleep(sleeptime)

    
    with open('{0}.txt'.format(filename),'a') as f:
        f.writelines('\n')

#####################################################

'''
pn = ['TRD5H10ENF-LF000', 'T-DQ4CNT-N00    ', 'T-DP4CNH-N00    ']


#1
CHM2T_client_400G()

time.sleep(20)

#2
for i in range(100):
    test('i2c_check_100_QSFPP',0) 
    
#3   
for i in range(100):
    logdata('cig_i2c', get_data(fr4_cig))
    with open('cig_i2c.txt','a') as f:
        f.writelines('\n')

for i in range(100):
    logdata('inn_fr4_i2c', get_data(fr4_inn))
    with open('inn_fr4_i2c.txt','a') as f:
        f.writelines('\n')

for i in range(100):
    logdata('inn_dr4_i2c', get_data(dr4_inn))
    with open('inn_dr4_i2c.txt','a') as f:
        f.writelines('\n')  
'''

