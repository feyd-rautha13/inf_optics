# /usr/bin/env python
# -*- coding : utf-8 -*-


__author__ = 'Sizhan Liu'
__version__ = "1.0"

'''
Driver for HP34970A
Reference: 
'''


class HP34970A(object):
    '''
    Driver for AG8164B, attenuator and power meter.
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
    def set_slot(self, ptype='K', slot = 202):
        self.write("CONF:TEMP TC,{0},(@{1})".format(ptype.upper(), slot))
        
    
    def get_temp(self, slot=202):
        
        self.write("ROUT:SCAN (@{0})".format(slot))
        temp = self.query("READ?")
        temp = self.data_parse(temp)
        temp = float(temp)
        return temp
        


    
    










