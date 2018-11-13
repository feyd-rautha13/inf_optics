# /usr/bin/env python
# -*- coding : utf-8 -*-

"""
Created on Sat Nov 10 15:46:53 2018
Modified on __________

Data process for passive component.
"""

__author__ = 'Sizhan Liu'
__version__ = "1.0"

import numpy as np
import pylab as pl


class channel(object):
    def __init__(self,channel_num,sp = 31.5, data_name_list = None, channel_plan = None):
        '''
        initial channel number, center frequency, center wavelength
        read data from file
        '''
        self._channel_num = channel_num
        
        self._channle_id_list = np.int0(channel_plan[0:,0])
        self._channel_plan_center = channel_plan[0:,1][self._channel_num-1]
        self._channel_plan_wavelength = channel_plan[0:,2][self._channel_num -1]
                 
        self._data_name_list = data_name_list
        self.__data = np.loadtxt(self._data_name_list[channel_num-1])
        
        self._sp = sp
        
        self.data_wavelength = self.__data[0:,0]
        self.data_freq = self.__data[0:,1]
        self.data_IL = self.__data[0:,2]
        self.data_GD = self.__data[0:,3]
        self.data_PDL = self.__data[0:,4]
        
            
        self.freq_cen_idx = self.find_nearest_index(self.data_freq, self._channel_plan_center)
        
        self.freq_sp_L_val = self._channel_plan_center - self._sp
        self.freq_sp_R_val = self._channel_plan_center + self._sp
        self.freq_sp_R_idx = self.find_nearest_index(self.data_freq, self.freq_sp_L_val)
        self.freq_sp_L_idx = self.find_nearest_index(self.data_freq, self.freq_sp_R_val)
        
        self.freq_cen_val = self.data_freq[self.freq_cen_idx]
        self.freq_cen_il_val = self.data_IL[self.freq_cen_idx]
    
    
    def channel_parameter(self):
        chn = self._channel_num
        freq = self._channel_plan_center
        wavelength = self._channel_plan_wavelength
        IL = self.freq_cen_il_val
        channel_parameter = [chn,freq, wavelength,IL]
        
        
        return channel_parameter
    
    def passband(self,xdB = 0):
        '''
        get 0.5/1/3 dB passband and clear channel passband, return a tuple
        '''
        freq_L_idx = self.find_nearest_index(self.data_IL[0:self.freq_cen_idx+1], self.freq_cen_il_val - xdB)
        freq_R_idx = self.find_nearest_index(self.data_IL[self.freq_cen_idx:], self.freq_cen_il_val - xdB) + self.freq_cen_idx
        
        freq_L_val = self.data_freq[freq_R_idx]
        freq_R_val = self.data_freq[freq_L_idx]
        
        ccp_band_L = np.abs(self.freq_cen_val - freq_L_val)
        ccp_band_R = np.abs(freq_R_val - self.freq_cen_val)
        
        xdB_passband = np.abs(self.data_freq[freq_L_idx] - self.data_freq[freq_R_idx])
        xdB_ccp_passband = 2*np.min([ccp_band_L, ccp_band_R])
        
        return freq_L_val, freq_R_val, xdB_passband, xdB_ccp_passband
    
    def gdr_cd(self, freq_L, freq_R, order = 2):
        '''
        Under discussion.
        '''
        idx_L = self.find_nearest_index(self.data_freq, freq_R)
        idx_R = self.find_nearest_index(self.data_freq, freq_L)
        
        wave_list = self.data_wavelength[idx_L:idx_R + 1]
        wave_list_poly = wave_list - self._channel_plan_wavelength
        gd_list = self.data_GD[idx_L:idx_R + 1] 
        
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
    def freq_shift(self):
        '''
        Get center frequecny shift, unit GHz
        '''
        freq_L_val = self.passband(3)[0]
        freq_R_val = self.passband(3)[1]
        real_freq = 0.5*(freq_L_val + freq_R_val)
        
        freq_shift = np.abs(self.freq_cen_val - real_freq)
        return freq_shift
    
    @property
    def pmd(self):
        '''
        polarization mode dispeersion, within SP.
        '''
        pmd_max = np.max(self.data_GD[self.freq_sp_L_idx : self.freq_sp_R_idx])
        pmd_min = np.min(self.data_GD[self.freq_sp_L_idx : self.freq_sp_R_idx])
        return pmd_max - pmd_min
    
    @property
    def il_ripple(self):
        '''
        Inserion loss ripple, within SP.
        '''
        il_max = np.max(self.data_IL[self.freq_sp_L_idx : self.freq_sp_R_idx])
        il_min = np.min(self.data_IL[self.freq_sp_L_idx : self.freq_sp_R_idx])
        return il_max - il_min
    
    @property
    def pdl(self):
        '''
        Polarization dependent loss, within SP.
        '''
        pdl = np.max(self.data_PDL[self.freq_sp_L_idx : self.freq_sp_R_idx])
        return pdl
    
    def optical_xtalk(self, band = 9):
        '''
        Get current channel cross talk for all channels
        '''
        xtalk = []
        freq_L = self._channel_plan_center - 9
        freq_R = self._channel_plan_center + 9
        
        for i in self._channle_id_list:
            
            channel_data = np.loadtxt(self._data_name_list[i-1])
            channel_data_freq = channel_data[0:,1]
            channel_data_IL = channel_data[0:,2]
            
            freq_L_idx = self.find_nearest_index(channel_data_freq, freq_R)
            freq_R_idx = self.find_nearest_index(channel_data_freq, freq_L)
            
            xtalk_i = np.max(channel_data_IL[freq_L_idx:(freq_R_idx+1)])
            xtalk.append(xtalk_i)
        return xtalk
    
    def xtalk(self, first_chn = 1, last_chn = 64, passband = 9):
        
        xtalk = self.optical_xtalk(passband)
        #channel_id = [int(x) for x in channel_id_list ]
        
        current_idx = self._channel_num - 1
        
        adj_chn_L = current_idx - 1
        adj_cha_R = current_idx + 1 
        
        n_adj_chn_L = current_idx - 2
        n_adj_chn_R = current_idx + 2
        
        adj_xtalk = []
        if adj_chn_L >= 0:
            adj_xtalk.append(xtalk[adj_chn_L])
        else:
            pass
        
        if adj_cha_R<=63:
            adj_xtalk.append(xtalk[adj_cha_R])
        else:
            pass
        
        adj_nxtalk = []
        if n_adj_chn_L>=0:
            adj_nxtalk.append(np.max(xtalk[0:(n_adj_chn_L+1)]))
        else:
            pass
        if n_adj_chn_R <= 63:
            adj_nxtalk.append(np.max(xtalk[n_adj_chn_R:64]))
       
        return np.max(adj_xtalk), np.max(adj_nxtalk)
        
        

#############################--commom methond--####################################    
    def find_nearest_index(self,array,value):
        '''
        find the nearest value index in an array
        '''
        index = (np.abs(array - value)).argmin()
        return index
    









    
