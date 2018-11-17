# /usr/bin/env python
# -*- coding : utf-8 -*-

"""
Created on Sat Nov 17 17:34:15 2018
Modified on 
File description: 
    
"""

__author__ = 'Sizhan Liu'
__version__ = "1.0"


import telnetlib
import time

class telnet(object):
    def __init__(self, host = '172.29.150.93', port = '11066', username = None, password = None):
        
        self._host = host
        self._port = port
        self._username = username
        self._pasword = password
        
        self.tn = telnetlib.Telnet()
        
        self.tn.open(self._host, self._port, 5 )
    
    def close(self):
        self.tn.close()
        print(self.__class__.__name__+ ' closed!')
        
    def write(self, cmd):
        cmd = str(cmd) + '\n'
        cmd = cmd.encode()
        self.tn.write(cmd)
        
    def read_raw(self):
        data = self.tn.read_some()
        return data
    
'''
ont603
'172.29.150.93'
port1 = 11066
port2 = 11067

'*PROMPT ON'
Query possible device
':PRTM:LIST?'

######### 业务配置 ##########
:INST:CONF:EDIT:OPEN ON   开始编辑

:INST:CONF:EDIT:LAY:STAC?

unframed bert = PHYS
100G_SR4 = PHYS_SR4FEC_PCSL_MAC
100G_LR4 = PHYS_PCSL_MAC
OTU4 = PHYS_OTL4_OTN
eg.

:INST:CONF:EDIT:LAY:STAC PHYS_OTL4_OTN

:INST:CONF:EDIT:APPL ON  应用

#########################

:ETIM? #持续时间
:ABOR;*WAI;:INIT:IMM:ALL;*WAI # 点Start

#######--Unframered bert 配置--###########

:SENS:DATA:TEL:PHYS:LINE:RATE?
:SENS:DATA:TEL:PHYS:LINE:RATE OTU3_E1
:SENS:DATA:TEL:PHYS:LINE:RATE ETH_40G
:SENS:DATA:TEL:PHYS:LINE:RATE OTU4
:SENS:DATA:TEL:PHYS:LINE:RATE ETH_100G
:SENS:DATA:TEL:PHYS:LINE:RATE OTU4


#############-traffic full load 配置-###############
:SOUR:DATA:TEL:MAC:TRAF:STAT? 
:SOUR:DATA:TEL:MAC:TRAF:STAT ON
:SOUR:DATA:TEL:MAC:TRAF:STAT OFF

配成百分百模式
:SOUR:DATA:TEL:MAC:TRAF:SCAL? 查模式
:SOUR:DATA:TEL:MAC:TRAF:SCAL SCALED 百分比模式
:SOUR:DATA:TEL:MAC:TRAF:SCAL ABSOLUTE 绝对值模式

配成100%
:SOUR:DATA:TEL:MAC:TRAF:BAND:USER:PERC?
:SOUR:DATA:TEL:MAC:TRAF:BAND:USER:PERC 100
'''
