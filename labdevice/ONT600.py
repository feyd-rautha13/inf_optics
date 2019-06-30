# /usr/bin/env python
# -*- coding : utf-8 -*-

"""
Created on Sun Jun 30, 17:20, 2019

Modified List:


File description: Viavi ONT-600 driver
    
"""

__author__ = 'Sizhan Liu'
__version__ = "1.0"

import sys
interface_path = 'D:\\work\\coding\\python\\inf_optics\\interface'
sys.path.append(interface_path)

from Telnetinterface import telnet

class ONT600_Mainframe(telnet):
    def __init__(self, host, port, timeout=5):
        self._host = host
        self._port = port
        self._timeout = timeout
        super().__init__(host = self._host, port = self._port, timeout = self._timeout )
        
        self.write('*prompt on')
        
        port_list = self.query(":PRTM:LIST?", '\n>')
        port_list = port_list.decode()      
        print(port_list)

        
class ONT600(telnet):
    def __init__(self, host, port, timeout=5):
        self._host = host
        self._port = port
        self._timeout = timeout
        super().__init__(host= self._host, port= self._port, timeout= self._timeout)
        self.write('*prompt on')
    
    def ont_query(self, cmd, prompt = '\n>'):
        
        return self.query(cmd, prompt)
    
    def close_session(self):
        self.close_telnet()        
        
    
        
'''
ont603
ip = '172.29.150.93'
port1 = 11066


'*PROMPT ON'
Query possible device
':PRTM:LIST?'

######### 业务配置 ##########
:INST:CONF:EDIT:OPEN ON   开始编辑

:INST:CONF:EDIT:LAY:STAC?
:INST:CONF:EDIT:LAY:STAC PHYS                 #Unframered Bert
:INST:CONF:EDIT:LAY:STAC PHYS_OTL4_OTN        #OTU4
:INST:CONF:EDIT:LAY:STAC PHYS_PCSL_MAC        #100GBE LR4
:INST:CONF:EDIT:LAY:STAC PHYS_SR4FEC_PCSL_MAC #100G SR4


:INST:CONF:EDIT:APPL ON  应用

#######--Unframered bert 配置--###########
测试数据配置
:SENS:DATA:TEL:PHYS:LINE:RATE?
:SENS:DATA:TEL:PHYS:LINE:RATE OTU3_E1
:SENS:DATA:TEL:PHYS:LINE:RATE ETH_40G
:SENS:DATA:TEL:PHYS:LINE:RATE OTU4
:SENS:DATA:TEL:PHYS:LINE:RATE ETH_100G
:SENS:DATA:TEL:PHYS:LINE:RATE OTU4



######################--40/100GBE 测试--####################

:SENS:DATA:TEL:PHYS:LINE:RATE?
:SENS:DATA:TEL:PHYS:LINE:RATE ETH_100G
:SENS:DATA:TEL:PHYS:LINE:RATE ETH_40G


:PHYS:PAYL:ALL:ASEC:LSS:BLOC?  #LOS 检测

#################--QSFP28 表现---##########################
打到High Power模式
:SOUR:DATA:TEL:PHYS:QSFP28:HIGH:POW:CL?
:SOUR:DATA:TEL:PHYS:QSFP28:HIGH:POW:CL ON
:SOUR:DATA:TEL:PHYS:QSFP28:HIGH:POW:CL OFF

:PHYS:TX:QSFP28:MSA:VEND:PNUM? #模块PN
:PHYS:TX:QSFP28:MSA:VEND:SNUM? #模块SN

I2C 速度
:SOUR:DATA:TEL:PHYS:CFP:MDIO:SPD?
:SOUR:DATA:TEL:PHYS:CFP:MDIO:SPD SLOW
:SOUR:DATA:TEL:PHYS:CFP:MDIO:SPD NORMAL
:SOUR:DATA:TEL:PHYS:CFP:MDIO:SPD FAST

Tx端
:OUTP:TEL:PHYS:LINE:OPT:STAT?
:OUTP:TEL:PHYS:LINE:OPT:STAT ON #光模块开光
:OUTP:TEL:PHYS:LINE:OPT:STAT OFF

Rx 端 
:PHYS:PAYL:ALL:ASEC:LSS:BLOC?  #LOS
:PHYS:PAYL:ALL:ECO:BIT:BLOC?   #误码数
:PHYS:PAYL:ALL:ERAT:BIT:BLOC?  #误码率


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

########## 点开始测试   ###########

:INIT:IMM:ALL;*WAI              # 点Start
:ABOR;*WAI                      #点stop
:ABOR;*WAI;:INIT:IMM:ALL;*WAI   #刷新
:ETIM? #持续时间 微秒
'''
    
