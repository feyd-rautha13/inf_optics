# /usr/bin/env python
# -*- coding : utf-8 -*-


__author__ = 'Sizhan Liu'
__version__ = "1.0"

'''
Driver for Anritsu 9710B Optical Spectrum Analyser.
MS9710B input/output buffer 256 byte.
'''
#import time
import re
import numpy as np

class MS9710B(object):
    '''
    Driver for MS9710B, Optical Spectrum Analyser.
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
#################### --data parse  -- ####################
    def data_parse(self, command):
        command = command.decode().replace("\r" , '')
        command = command.replace("\n" , '')
        return command
    

################ -- Wavelength -- ######################
    @property
    def osaCntWav(self):
        wave = self.query("CNT?")
        wave = self.data_parse(wave)
        wave = float(wave)
        return wave
    
    @property
    def osaStaWav(self):
        wave = self.query("STA?")
        wave = self.data_parse(wave)
        wave = float(wave)
        return wave
    @osaStaWav.setter
    def osaStaWav(self, startwave):
        startwave = str(startwave)
        cmd = "STA " + startwave
        self.write(cmd)
    
    @property
    def osaStoWav(self):
        wave = self.query("STO?")
        wave = self.data_parse(wave)
        wave = float(wave)
        return wave
    @osaStoWav.setter
    def osaStoWav(self, startwave):
        startwave = str(startwave)
        cmd = "STO " + startwave
        self.write(cmd)

############## --Device Setting-- #############
    @property
    def osaRes(self):
        '''
        MS9710B resolution, unit is nm
        '''
        res = self.query("RES?")
        res = self.data_parse(res)
        res = float(res)
        return res
    @osaRes.setter
    def osaRes(self, res = 0.1):
        '''
        set resolution, unit nm.
        MS9710B resolution could be 0.05, 0.07, 0.1, 0.2, 0.5, 1.
        '''
        res = str(res)
        res = "RES " + res
        self.write(res)
    
    @property
    def osaVBW(self):
        '''
        MS9710B vbw, unit Hz.
        '''
        vbw = self.query("VBW?")
        vbw = self.data_parse(vbw)
        if vbw == '10HZ': vbw = 10
        elif vbw == '100HZ' : vbw = 100
        elif vbw == '1KHZ' : vbw = 1000
        elif vbw == '10KHZ' : vbw = 1E4
        elif vbw == '100KHZ' : vbw = 1E5
        else : vbw = 1E6
        return vbw
    @osaVBW.setter
    def osaVBW(self, vbw):
        '''
        set MS9710B vbw.
        MS9710B vbw must be 1MHz, 100KHz, 10kHz, 1kHz, 100Hz, 10Hz
        '''
        vbw = str(vbw)
        vbw = "VBW " + vbw
        self.write(vbw)
        
    @property
    def osaMPT(self):
        '''
        MS9710 sampling points, no unit.
        '''
        mpt = self.query('MPT?')
        mpt = self.data_parse(mpt)
        return int(mpt)
    @osaMPT.setter
    def osaMPT(self,mpt):
        '''
        set MS9710B sampling points.
        MS9710B sampling points must be 51,101,251,501,1001,2001,5001.
        '''
        mpt = str(mpt)
        mpt = 'mpt ' + mpt
        self.write(mpt)
        
    
################## ---Get trace -- ###############################
    def osaGet_Y(self):
        '''
        return Y_axis value in unit dBm
        '''
        endflag = b'\r\r\n'
        endnumber = 3
        
        Y_axis = self.query("DMA?", endflag, endnumber)
        Y_axis = re.split(r";|\r|\n", Y_axis.decode())
        Y_axis = [x for x in Y_axis if x != '']
        Y_axis = np.array([float(x) for x in Y_axis])
        return Y_axis
    
    def osaGet_X(self):
        '''
        return X_axis value in unit nm
        '''
        X_axis = np.linspace(int(self.osaStaWav), int(self.osaStoWav), self.osaMPT)
        return X_axis



'''
osa.write("SSI")  #do a sigle sweep
osa.query("ESR2?")  #check if finished

Y = osa.osaGet_Y()

X = osa.osaGet_X()

z = np.array([X,Y])


pl.plot(z[0,:], z[1,:], label = "Lwdm"),pl.legend()
'''
