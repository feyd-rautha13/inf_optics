# /usr/bin/env python
# -*- coding : utf-8 -*-

'''
Data process for AWG component.
'''

"""
---------------- Rev histroy --------------
Rev1.0	Sat Nov 10 15:46:53 2018
first draft.

Rev1.1	Fri Jan 18 15:54 2019
Add ITU-T channel plan format and data format.
Re-write AWG class

"""
__author__ = 'Sizhan Liu'
__version__ = "1.1"

'''
==============================================================
ITU-T channel plan format (from Specification)
--------------------------------------------------------------
|0               |1                     |2
|channel number  |ITU-T Freq(increase)  |ITU-T Wave(de-crease)
|----------------|----------------------|---------------------
|1	             |191362.5	            |1566.620722
|2				 |191437.5				|1566.006963
|3				 |191512.5				|1565.393684
|..				 |..					|..
|..				 |..					|..
|63				 |196012.5				|1529.455815
|64				 |196087.5				|1528.870826

======================================================================================================
component data and calibration data format(from Luna)
Luna give a reverse data column
------------------------------------------------------------------------------------------------------
|0                       |1                      |2              |3      |4      |5          |6  
|Wavelength(increas)     |Frequency(decrease)    |GD 			 |PDL    |PMD    |Max Loss   |Min Loss
|------------------------|-----------------------|---------------|-------|-------|-----------|--------
|1527.38				 |196279.04 			 |3274.74		 |11.74	 |1.34 	 |-56.68 	 |-68.42 
|1527.38				 |196278.88 			 |3268.32		 |8.32 	 |23.23  |-58.54 	 |-66.86 
|..				 		 |..					 |.. 			 |..	 |..	 |..		 |..
|..				 		 |..					 |.. 			 |..	 |..	 |..		 |..
|1569.18				 |191050.20				 |3168.74 		 |9.87 	 |27.23  |-49.78 	 |-59.65 
|1569.18				 |191050.04				 |3186.12 		 |11.81	 |3.69 	 |-51.50 	 |-63.31 
|1569.18				 |191049.88				 |3222.92 		 |13.50	 |-0.12  |-53.86 	 |-67.36 
======================================================================================================
'''
import numpy as np
#import pylab as pl
#import os




class AWG(object):
    def __init__(self,channel_num, sp = 31.5, data_name_list = None, channel_plan = None):
        '''
        initial channel number, center frequency, center wavelength
        read data from file
        '''
        #initial channel ID and specification passband
        self._channel_num = channel_num

        self._sp = sp
        
        # channel plan csv file analyser
        self._channle_plan_id_list = np.int0(channel_plan[0:,0])
        self._channel_plan_center_freq_list = channel_plan[0:,1]
        self._channel_plan_center_wavelength_list = channel_plan[0:,2]
        
        # current channel plan paramter
        self._cr_id = self._channle_plan_id_list[self._channel_num-1]
        self._cr_freq_cen_val = self._channel_plan_center_freq_list[self._channel_num-1]
        self._cr_wave_cen_val = self._channel_plan_center_wavelength_list[self._channel_num-1]
        
        self._cr_freq_sp_L_val = self._channel_plan_center_freq_list[self._channel_num-1] - self._sp
        self._cr_freq_sp_R_val = self._channel_plan_center_freq_list[self._channel_num-1] + self._sp
        
        #luna data parse        
        self._data_name_list = data_name_list
        self.__data = np.loadtxt(self._data_name_list[channel_num-1])
        
        wav = 0
        freq = 1
        gd = 2
        pdl = 3
        pmd = 4
        mxlos = 6
        mnlos = 5

        self.data_wavelength = self.__data[0:,wav]
        self.data_freq = self.__data[0:,freq]
        self.data_GD = self.__data[0:,gd]
        self.data_PDL = self.__data[0:,pdl]
        self.data_PMD = self.__data[0:,pmd]
        self.data_Max_Loss = self.__data[0:,mxlos]
        self.data_Min_Loss = self.__data[0:,mnlos]
        self.data_IL = 0.5*(self.data_Max_Loss + self.data_Min_Loss)
        
        # Confirm centre frequency, sp_l, sp_R index  from test data
        self.data_freq_cen_idx = self.find_nearest_index(self.data_freq, self._cr_freq_cen_val)
        self.data_freq_sp_L_idx = self.find_nearest_index(self.data_freq, self._cr_freq_sp_R_val)
        self.data_freq_sp_R_idx = self.find_nearest_index(self.data_freq, self._cr_freq_sp_L_val)
        
        #Confirm center frequecy, sp_L, sp_R value from test data
        self.data_il_cen_val = self.data_IL[self.data_freq_cen_idx]
        self.data_freq_cen_val = self.data_freq[self.data_freq_cen_idx]    
        self.data_freq_sp_L_val = self.data_freq[self.data_freq_sp_L_idx]
        self.data_freq_sp_R_val = self.data_freq[self.data_freq_sp_R_idx]

    
    
    def channel_parameter(self):
        chn = self._cr_id
        center_freq = self._cr_freq_cen_val
        center_wavelength = self._cr_wave_cen_val
        
        return chn, center_freq, center_wavelength
    
    def IL(self):
        IL_cen = self.data_il_cen_val
        IL_worst_case = np.min(self.data_Max_Loss[self.data_freq_sp_L_idx:self.data_freq_sp_R_idx])
        IL_best_case = np.max(self.data_Min_Loss[self.data_freq_sp_L_idx:self.data_freq_sp_R_idx])
        IL_ripple =np.abs( IL_worst_case - IL_best_case)
        
        return IL_cen, IL_best_case, IL_worst_case, IL_ripple
        
    
    def passband(self,xdB = 0):
        '''
        get 0.5/1/3 dB passband and clear channel passband, return a tuple
        '''
        freq_L_idx = self.find_nearest_index(self.data_IL[0:self.data_freq_cen_idx+1], self.data_il_cen_val - xdB)
        freq_R_idx = self.find_nearest_index(self.data_IL[self.data_freq_cen_idx:], self.data_il_cen_val - xdB) + self.data_freq_cen_idx
        
        freq_L_val = self.data_freq[freq_R_idx]
        freq_R_val = self.data_freq[freq_L_idx]
        
        ccp_band_L = np.abs(self._cr_freq_cen_val - freq_L_val)
        ccp_band_R = np.abs(freq_R_val - self._cr_freq_cen_val)
        
        xdB_passband = np.abs(self.data_freq[freq_L_idx] - self.data_freq[freq_R_idx])
        xdB_ccp_passband = 2*np.min([ccp_band_L, ccp_band_R])
        xdB_wave_accuracy = 0.5*(ccp_band_R - ccp_band_L)
        
        return freq_L_val, freq_R_val, xdB_passband, xdB_ccp_passband, xdB_wave_accuracy
    
    def gdr_cd(self, order = 2):
        '''
        Under discussion.
        '''
        wave_list = self.data_wavelength[self.data_freq_sp_L_idx : (self.data_freq_sp_R_idx+1)]
        wave_list_poly = wave_list - self._cr_wave_cen_val
        gd_list = self.data_GD[self.data_freq_sp_L_idx : (self.data_freq_sp_R_idx+1)] 
        
        polynomial = np.polyfit(wave_list_poly, gd_list, order)
        p1 = np.poly1d(polynomial)
        gd_list_poly = p1(wave_list_poly)
        
        
        gdr_list = gd_list - gd_list_poly
        gdr = gdr_list[np.abs(gdr_list).argmax()]
        
#        pl.plot(wave_list, gd_list, label='Init'),pl.plot(wave_list, gd_list_poly, label = 'Fit')
#        pl.show()
#        
#        print(p1)              
#        print( polynomial[1], gdr)
        if order == 1:
            return polynomial[0], gdr
        elif order == 2:
            return polynomial[1], gdr
        else:
            print('fail')
 
    
    @property
    def pmd(self):
        '''
        polarization mode dispeersion, within SP.
        '''
        pmd_max = np.max(self.data_GD[self.data_freq_sp_L_idx : self.data_freq_sp_R_idx])
        pmd_min = np.min(self.data_GD[self.data_freq_sp_L_idx : self.data_freq_sp_R_idx])
        return pmd_max - pmd_min
    
    
    @property
    def pdl(self):
        '''
        Polarization dependent loss, within SP.
        '''
        pdl = np.max(self.data_PDL[self.data_freq_sp_L_idx : self.data_freq_sp_R_idx])
        return pdl
    
    def optical_xtalk(self, band = 9):
        '''
        Get current channel cross talk for all channels
        '''
        xtalk = []
        freq_L = self._cr_freq_cen_val - band
        freq_R = self._cr_freq_cen_val + band
        
        for i in self._channle_plan_id_list:
            
            channel_data = np.loadtxt(self._data_name_list[i-1])
            channel_data_freq = channel_data[0:,1]
            channel_data_IL = 0.5*(channel_data[0:,5] + channel_data[0:,6])
            
            freq_L_idx = self.find_nearest_index(channel_data_freq, freq_R)
            freq_R_idx = self.find_nearest_index(channel_data_freq, freq_L)
            
            xtalk_i = np.max(channel_data_IL[freq_L_idx:(freq_R_idx+1)])
            xtalk.append(xtalk_i)
        return xtalk
    
    def xtalk(self, first_chn = 1, last_chn = 64, passband = 9):
        
        xtalk = self.optical_xtalk(passband)
        #channel_id = [int(x) for x in channel_id_list ]
        
        current_chn_idx = self._channel_num - 1
        first_chn_idx = first_chn - 1
        last_chn_idx = last_chn - 1
        
        adj_chn_L_idx = current_chn_idx - 1
        adj_chn_R_idx = current_chn_idx + 1 
        
        n_adj_chn_L_idx = current_chn_idx - 2
        n_adj_chn_R_idx = current_chn_idx + 2
        
        adj_xtalk = 0
        n_adj_xtalk = 0
        
        if adj_chn_L_idx < first_chn_idx :
            adj_xtalk_L = None
            adj_xtalk_R = xtalk[adj_chn_R_idx]
            adj_xtalk = adj_xtalk_R

        elif adj_chn_R_idx > last_chn_idx :
            adj_xtalk_L = xtalk[adj_chn_L_idx]
            adj_xtalk_R = None
            adj_xtalk = adj_xtalk_L
        else:
            adj_xtalk_L = xtalk[adj_chn_L_idx]
            adj_xtalk_R = xtalk[adj_chn_R_idx]
            adj_xtalk = np.max([adj_xtalk_L, adj_xtalk_R])
            
        if n_adj_chn_L_idx < first_chn_idx:
            n_adj_xtalk_L = None
            n_adj_xtalk_R = np.max(xtalk[n_adj_chn_R_idx:(last_chn_idx+1)])
            n_adj_xtalk = n_adj_xtalk_R

        elif n_adj_chn_R_idx > last_chn_idx:
            n_adj_xtalk_L = np.max(xtalk[first_chn_idx: n_adj_chn_L_idx+1])
            n_adj_xtalk_R = None
            n_adj_xtalk = n_adj_xtalk_L
        else:
            n_adj_xtalk_L = np.max(xtalk[first_chn_idx:n_adj_chn_L_idx+1])
            n_adj_xtalk_R = np.max(xtalk[n_adj_chn_R_idx:last_chn_idx+1])
            n_adj_xtalk = np.max([n_adj_xtalk_L, n_adj_xtalk_R])
        
        adj_xtalk1 = self.data_il_cen_val - adj_xtalk
        n_adj_xtalk1 = self.data_il_cen_val - n_adj_xtalk
      
        return adj_xtalk1, n_adj_xtalk1
        
        

#############################--commom methond--####################################    
    def find_nearest_index(self,array,value):
        '''
        find the nearest value index in an array
        '''
        index = (np.abs(array - value)).argmin()
        return index
    