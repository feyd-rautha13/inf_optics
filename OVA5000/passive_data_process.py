# /usr/bin/env python
# -*- coding : utf-8 -*-

"""
Created on Sat Nov 10 15:46:53 2018
Modified on __________

Data process for passive component.
"""

__author__ = 'Sizhan Liu'
__version__ = "1.0"

import os
import numpy as np

csv_path = "C:\\Data\\sliu3\\Documents\\work\\coding\\python\\OpticalTest\\OMD64\\channelplan.csv"
data_path = "C:\\Data\\sliu3\\Documents\\work\\coding\\python\\OpticalTest\\OMD64\\mux_data"
keywords = 'mux'


def channel_plan(path):
    '''
    Get channel plan from csv file. 
    coloum 0 = channel id
    coloum 1 = center frequency unit = Ghz
    coloum 2 = center wavelength unit = nm
    '''    
    channel_plan = np.loadtxt(path, delimiter = ',', usecols=(0,1,2))
    return channel_plan


def get_data_list(path = None, keywrods = None):
    '''
    Get data file name list 
    '''
    data_list = os.listdir(path)
    data_list = [x for x in data_list if keywords in x]
    return data_list


channel_id_list = channel_plan(csv_path)[0:,0]
center_freq_list = channel_plan(csv_path)[0:,1]
data_name_list = get_data_list(data_path)

class channel(object):
    def __init__(self,channel_num,sp = 31.5):
        
        channel_plan_center = center_freq_list[channel_num-1]
        
        self.__data = np.loadtxt(data_name_list[channel_num-1])
        self._channel_num = channel_num
        self._sp = sp
        
        self.data_freq = self.__data[0:,1]
        self.data_IL = self.__data[0:,2]
        self.data_GD = self.__data[0:,3]
        self.data_PDL = self.__data[0:,4]
            
        self.freq_cen_idx = self.find_nearest_index(self.data_freq, channel_plan_center)
        self.freq_sp_R_idx = self.find_nearest_index(self.data_freq, channel_plan_center - self._sp)
        self.freq_sp_L_idx = self.find_nearest_index(self.data_freq, channel_plan_center + self._sp)
        
        self.freq_cen_val = self.data_freq[self.freq_cen_idx]
        self.freq_cen_il_val = self.data_IL[self.freq_cen_idx]
    
    @property
    def channel_id(self):
        return self._channel_num
    
    def passband(self, xdB = 0):
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
    

  
    @property
    def freq_shift(self):
        '''
        Get center frequecny shift, unit GHz
        '''
        freq_L_val = self.xdB_p(3)[0]
        freq_R_val = self.xdB_p(3)[1]
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
        
#############################--commom methond--####################################    
    def find_nearest_index(self,array,value):
        '''
        find the nearest value index in an array
        '''
        index = (np.abs(array - value)).argmin()
        return index
    
    
