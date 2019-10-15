# /usr/bin/env python
# -*- coding : utf-8 -*-


__author__ = 'Sizhan Liu'
__version__ = "1.0"
'''
first version of github
'''

'''
Driver for Agilent Technologies,8164B
'''

class AG8164B(object):
    '''
    Driver for AG8164B, attenuator and power meter.
    '''
    def __init__(self, GPIBaddress, interface):
        '''
        interface is a prologix case
        '''
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
    
#############################################################
    def slotID(self, slot):
        '''
        For agilent 8164B, slot from 1 to 4.
        '''
        cmd = ":SLOt"+str(slot)+":IDN?"
        return self.query(cmd)    

#################### --data parse  -- ####################
    def data_parse(self, command):
        command = command.decode().replace("\r" , '')
        command = command.replace("\n" , '')
        return command

################-- Attenuator command --###########################
    @property
    def attValue(self):
        return self.query("INP1:ATT?")
    @attValue.setter
    def attValue(self,value):
        value = "INP1:ATT "+str(value)
        self.write(value)
    
    @property
    def attOutPutPower(self):
        power = self.query("outp1:pow?")
        power = self.data_parse(power)
        power = float(power)
        return power  
    @attOutPutPower.setter
    def attOutPutPower(self, power):
        power = str(power)
        cmd = "OUTP1:POW " + power
        self.write(cmd)

    @property
    def attWav(self):
        wavelength = self.query("inp1:wav?")
        wavelength = self.data_parse(wavelength)
        wavelength = float(wavelength)
        return wavelength
    @attWav.setter
    def attWav(self, wavelength):
        wavelength = str(wavelength)
        cmd = "inp1:wav " + wavelength+"nm"
        self.write(cmd)

    @property
    def attwavOffset(self):
        offset = self.query("inp1:offs?")
        offset = self.data_parse(offset)
        offset = float(offset)
        return offset
    @attwavOffset.setter
    def attwavOffset(self, offset):
        offset = str(offset)
        cmd = "INP1:OFFS " + offset + "dB"
        self.write(cmd)

    @property
    def attShutter(self):
        cmd = "OUTP1:STAT?"
        shutter_status = self.query(cmd)
        shutter_status = self.data_parse(shutter_status)
        return shutter_status
    @attShutter.setter
    def attShutter(self, status=0):
        status = str(status)
        cmd = "OUTP1:STAT " + status
        self.write(cmd)

############### -- Power meter command --##########################
    @property
    def pmPower(self):
        power = self.query(":READ3:POW?")
        power = self.data_parse(power)
        power = float(power)
        return power   
    @property
    def pmWav(self):
        wavelength = self.query("sens3:pow:wav?")
        wavelength = self.data_parse(wavelength)
        wavelength = float(wavelength)
        return wavelength
    @pmWav.setter
    def pmWav(self, wavelength):
        wavelength = str(wavelength)
        cmd = "sens3:pow:wav " + wavelength+"nm"
        self.write(cmd)


























