# /usr/bin/env python
# -*- coding : utf-8 -*-


__author__ = 'Sizhan Liu'
__version__ = "1.0"

'''
Driver for Dicon HP86060C, optical Switch
Reference: 
'''

#----- Add lib path ------
interface_path = "D:\\work\\coding\\python\\inf_optics\\interface"
component_path = "D:\\work\\coding\\python\\inf_optics\\Test\\component"
device_path = "D:\\work\\coding\\python\\inf_optics\\labdevice"

import sys
sys.path.append(interface_path)
sys.path.append(component_path)
sys.path.append(device_path)


from prologix import Prologix

prologix_ip = '172.29.150.127'
prologix_port = 1234
GPIB_86060C = 19

prologix = Prologix(prologix_ip, prologix_port)

class HP86060C(object):
    '''
    Driver for HP86060C, attenuator and switch.
    '''
    def __init__(self, GPIBaddress, interface):
        self._gpibaddress = GPIBaddress
        self.dev = interface

########## --super class alternative method --- #######
    def write(self,cmd):
        self.dev.setAddr(self._gpibaddress)
        self.dev.write(cmd)
    
    def query(self, cmd, flag = None, endnumber = None):
        self._flag = flag
        self._endnumber = endnumber
        
        self.dev.setAddr(self._gpibaddress)
        if self._flag == None:
            data = self.dev.query(cmd)
        else:
            data = self.dev.query(cmd, self._flag, self._endnumber)
        return data
    
    def data_parse(self,data):
        return data.decode().replace('\n','')
##########################################################

    @property
    def deviceID(self):
        return self.query("*IDN?")
        
##########################################################
    @property
    def MSwitchChannel(self):
        pass
    @MSwitchChannel.setter
    def MSwitchChannel(self, channel):
        '''
        channel = [1:6]
        '''
        cmd = ':ROUTE:LAYER1:CHANNEL A1,B{0}'.format(channel)
        self.write(cmd)
        
    def MSwitchByPass(self):
        cmd = ':ROUTE:LAYER1:CHANNEL A1,B0'
        self.write(cmd)
    
    def MSwitchStatus(self):
        cmd = 'SYSTEM:CONFIG?'
        return self.data_parse(self.query(cmd))
        


    
    










