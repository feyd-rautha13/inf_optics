# /usr/bin/env python
# -*- coding : utf-8 -*-

#-------------------------------------------------------------------------------
# Name:        "ANDO,AQ6317 OSA"
# Purpose:     Optical Test in ShangHai Lab
#
# Author:      Youbin Zheng/Sizhan Liu
# Reference    Yingkan Chen's Prologix controller
# Version:     1.0
#
# Created:     12/03/2018
# Modify:      12/03/2018
# Copyright:   (c) Infinera Shanghai R&D
#-------------------------------------------------------------------------------

import numpy as np
#AQ6317 Optical Spectrum Analyzer

class AQ6317(object):
    '''
    AQ6317 remote control
    '''
    def __init__(self, selfaddress, interface):
        '''
        interface is a prologix case
        '''
        self._selfaddress = selfaddress
        self.dev = interface

########## --super class alternative method --- #######
    def write(self,cmd):
        self.dev.setAddr(self._selfaddress)
        self.dev.write(cmd)
    

    def query(self, cmd, flag = None, endnumber = None):
        self._flag = flag
        self._endnumber = endnumber
        
        self.dev.setAddr(self._selfaddress)

        if self._flag == None:
            data = self.dev.query(cmd)
        else:
            data = self.dev.query(cmd, self._flag, self._endnumber)
        return data
		
##########################################################
    @property
    def deviceID(self):
        return self.query("*IDN?")
    
    @property
    def Init(self):
        self.write("INIT")
        
    @property
    def RST(self):
        self.write("*RST")
        
#################### --data parse  -- ####################
    def data_parse(self, command):
        command = command.decode().replace("\r" , '')
        command = command.replace("\n" , '')
        return command
    

		
################ -- Wavelength -- ######################
    @property
    def CntWav(self):
        wave = self.query("CTRWL?")
        wave = self.data_parse(wave)
        wave = float(wave)
        return wave
    
    @property
    def StaWav(self):
        wave = self.query("STAWL?")
        wave = self.data_parse(wave)
        wave = float(wave)
        return wave
    @StaWav.setter
    def StaWav(self, startwave):
        startwave = str(startwave)
        cmd = "STAWL " + startwave
        self.write(cmd)
    
    @property
    def StoWav(self):
        wave = self.query("STPWL?")
        wave = self.data_parse(wave)
        wave = float(wave)
        return wave
    @StoWav.setter
    def StoWav(self, startwave):
        startwave = str(startwave)
        cmd = "STPWL" + startwave
        self.write(cmd)

############## --Device Setting-- #############
    @property
    def Res(self):
        '''
        MS9710B resolution, unit is nm
        '''
        res = self.query("RESLN?")
        res = self.data_parse(res)
        res = float(res)
        return res
    @Res.setter
    def Res(self, res = 0.1):
        '''
        set resolution, unit nm.
        MS9710B resolution could be 0.05, 0.07, 0.1, 0.2, 0.5, 1.
        '''
        res = str(res)
        res = "RESLN " + res
        self.write(res)
    
    @property
    def VBW(self):
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
    @VBW.setter
    def VBW(self, vbw):
        '''
        set MS9710B vbw.
        MS9710B vbw must be 1MHz, 100KHz, 10kHz, 1kHz, 100Hz, 10Hz
        '''
        vbw = str(vbw)
        vbw = "VBW " + vbw
        self.write(vbw)
        
    @property
    def MPT(self):
        '''
        MS9710 sampling points, no unit.
        '''
        mpt = self.query('SEGP?')
        mpt = self.data_parse(mpt)
        return int(mpt)
    @MPT.setter
    def MPT(self,mpt):
        '''
        set MS9710B sampling points.
        MS9710B sampling points must be 51,101,251,501,1001,2001,5001.
        '''
        mpt = str(mpt)
        mpt = 'SMPL ' + mpt
        self.write(mpt)
        
    
################## ---Get trace -- ###############################
#    def Get_Y(self):
#        '''
#        return Y_axis value in unit dBm
#        '''
#        endflag = b'\r\r\n'
#        endnumber = 3
#        
#        Y_axis = self.query("DMA?", endflag, endnumber)
#        Y_axis = re.split(r";|\r|\n", Y_axis.decode())
#        Y_axis = [x for x in Y_axis if x != '']
#        Y_axis = np.array([float(x) for x in Y_axis])
#        return Y_axis
        
    def Get_Y(self):
    
        endflag = b'\r\r\n'
        endnumber = 3
        
        Y_axis = self.query("DMA?", endflag, endnumber)
        Y_axis = re.split(r";|\r|\n", Y_axis.decode())
        Y_axis = [x for x in Y_axis if x != '']
        Y_axis = np.array([float(x) for x in Y_axis])
        return Y_axis
    
    
    def Get_X(self):
        '''
        return X_axis value in unit nm
        '''
        X_axis = np.linspace(int(self.StaWav), int(self.StoWav), self.MPT)
        return X_axis


#set sweep   
    def SignleWeep(self):
        self.write("SGL")
    def AutoSweep(self):
        self.write("AUTO")
    def RepeatSweep(self):
        self.write("PRT")
    def StopSweep(self):
        self.write("STP")
        
#set wavelength
    def SetCenterWavelength(self,wavelength):
        Keywords = "CTRWL"+str(wavelength)
        self.write(Keywords)
    def SetStartWavelength(self,wavelength):
        Keywords = "STAWL"+str(wavelength)
        self.write(Keywords)
    def SetStopWavelength(self,wavelength):
        Keywords = "STPWL"+str(wavelength)
        self.write(Keywords)    
    def SetAutoCenter(self):
        self.write("ATCR*")
    def SetPeakasCenter(self):
        self.write("CTR=P")

#set REF Level
    def SetRefLevle(self,power):
        Keywords = "REFL" + str(power)   
        self.write(Keywords)
    def GetRelLevel(self):
        return self.ask("RELF?")
    def SetPeakAsRef(self):
        self.write("REF=P")
        
# set Axis Scale
    def SetAxisYScale(self,scale):
        Keywords = "LSCL"+str(scale)
        self.write(Keywords)
    def GetAxisYScale(self):
        return self.ask("LSCL?")
    def SetAxisXScale(self,scale):
        Keywords = "BASL"+str(scale)
        self.write(Keywords)
    def GetAxisXScale(self):
        return self.ask("BASL?")

# set Test Parameter
    def SetRes(self,resl=0.01):
        Keywords = "RESLN"+str(resl)
        self.write(Keywords)
    def GetRes(self):
        return self.ask("RESLN?") 
    def SetAvg(self,times=1):
        Keywords = "AVG" + str(times)
        self.write(Keywords)
    def GetAvg(self):
        return self.ask("AVG?")    
    def SetSP(self,points=0):
        Keywords = "SMPL" + str(points)
        self.write(Keywords)
    def SetMearSens(self,sen = "SNAT"):
        self.write(sen)
    def GetMearSens(self):
        return self.ask("SENS?")

# Peak Search
    def PeakSearch(self):
        self.write("PKSR")
    def NextLargestSearch(self):
        self.write("NSR")

# DFB-LD analyse
# Important
    def DFBAnalyse(self):
        self.write("DFBAN")