# /usr/bin/env python
# -*- coding : utf-8 -*-


__author__ = 'Sizhan Liu'
__version__ = "1.0"

'''
Driver for HP8152A
Reference: youbin's 8152A driver
'''

class HP8152A(object):
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
##########################################################

    @property
    def deviceID(self):
        return self.query("*IDN?")
        
##########################################################
    
    @property
    def power(self):
        cmd = "Pwmtr"
        data = self.query(cmd)
        data = float(data.decode().replace('\r\n',""))

        return data
    
    @property
    def wav(self):
        cmd = "WVL?1"
        data = self.query(cmd)
        data = float(data.decode().replace('\r\n',""))*1E9
        return data
    @wav.setter
    def wav(self, wavelength = 1550):
        cmd="WVL1,"+str(wavelength)+"nm" 
        self.write(cmd)
        
     
    
    
    










