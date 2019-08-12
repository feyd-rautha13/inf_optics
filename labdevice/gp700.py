# /usr/bin/env python
# -*- coding : utf-8 -*-


__author__ = 'Sizhan Liu'
__version__ = "1.0"

'''
Driver for Dicon GP700
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
GPIB_gp700 = 30

prologix = Prologix(prologix_ip, prologix_port)

class GP700(object):
    '''
    Driver for GP700, attenuator and switch.
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
        return self.data_parse(self.query("*IDN?"))
        
############# ---Multi Switch 1x6 --- #########################
    @property        
    def MSwitchChannel(self):
        cmd = 'M1?'
        value = self.data_parse(self.query(cmd))
        inchannel = int(value[2])
        outchannel = int(value[0])
        if outchannel == 0:
            return 'Switch Bypass.'
        else:
            return 'Input channel M{0}, output channel {1}'.format(inchannel, outchannel)
    @MSwitchChannel.setter
    def MSwitchChannel(self, channel):
        '''
        channel = [1:6]
        '''
        cmd = 'M1 {0}'.format(channel)
        self.write(cmd)
        
    def MSwitchByPass(self):
        cmd = 'M1 0'
        self.write(cmd)
    

        
################ ---Attenuator Switch--- ##############
    @property
    def AttValue(self):
        cmd = 'A1?'
        value = self.data_parse(self.query(cmd))
        return float(value)
    @AttValue.setter
    def AttValue(self, value):
        cmd = 'A1 {0}'.format(value)
        self.write(cmd)

################ -- 1x2 Switch -- #####################
    def SSwitchStatus(self, port=1):
        cmd = "P{0}?".format(port)
        value = int(self.data_parse(self.query(cmd))) - 1
        value = format(value, '#06b')
        return value[-4:], int(value,2)
    
    def SSwitchOut1(self, card=1, port=1):
        '''
        card = [1:3]
        port = [1:4]
        '''
        status = self.SSwitchStatus(card)[1]
        value = 1<<(port-1)
        #Or by bits
        value = (status|value) + 1 
        cmd = 'P{0} {1}'.format(card, value)
        
        self.write(cmd)
        
    def SSwitchOut2(self, card=1, port=1):
        '''
        card = [1:3]
        port = [1:4]
        '''
        status = self.SSwitchStatus(card)[1]     
        value = 0xF - (1<<(port-1))
        #And by bits
        value = (value & status) + 1
        cmd = 'P{0} {1}'.format(card, value)
        self.write(cmd)


    
    










