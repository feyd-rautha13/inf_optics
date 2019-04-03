# /usr/bin/env python
# -*- coding : utf-8 -*-

'''
Data process for WSS component.
'''

"""
---------------- Rev histroy --------------
Rev1.0	Fri Mar 29 9:50 2019


"""
__author__ = 'Sizhan Liu'
__version__ = "1.1"

import numpy as np
import pylab as pl

even_trace = "D:\\project\\OFP2\\2018-04-27 WSS\\2019-03-29 data\\f_50G\\Port4\\f_even_50G_0dB.txt"
odd_trace = "D:\\project\\OFP2\\2018-04-27 WSS\\2019-03-29 data\\f_50G\\Port4\\f_odd_50G_0dB.txt"
channel_plan_path = "D:\\project\\OFP2\\2018-04-27 WSS\\test\\code\\channelplan_50G.csv "


class WSS(object):
    def __init__(self, passband_id, channel_plan, Eventrace, Oddtrace, sp_pass, sp_block, sp_grid):
        '''
        channnel_id, int, current analyse channel id.
        channel_plan: csv file, channel number and centerfrequency
        Eventrace: txt file,even trace from luna raw data
        Oddtrace: txt file, odd trace from luna raw data
        sp_pass: float, specification band for pass band, unit = GHz
        sp_block: float, specification band for block band, unit = GHz
        sp_grid: float, grid for channel plan, unit = GHz
        '''
        #Get raw data, channel plan, even trace data and odd trace data
        chn_plan = np.loadtxt(channel_plan, delimiter = ',', usecols=(0,1,2))
        even_data = np.loadtxt(Eventrace)
        odd_data = np.loadtxt(Oddtrace)
        
        #Seperate channel id and channel frequency from channel plan
        self.all_chn_id = [int(x) for x in chn_plan[0:,0]]
        self.all_chn_freq = chn_plan[0:,1]
        self.all_chn_wav = chn_plan[0:,2]
        

        self.sp_pass = sp_pass
        self.sp_block = sp_block
        self.sp_grid = 0.5 * sp_grid
        
        wav = 0
        freq = 1
        gd = 2
        pdl = 3
        pmd = 4
        mxlos = 6
        mnlos = 5        
        
        #Set DUT channel, id, center frequency, pass band, block band, gird band frequency value
        self._ITU_id = passband_id
        self._ITU_freq_cen_val = self.all_chn_freq[self._ITU_id]
        self._ITU_wave_cen_val = self.all_chn_wav[self._ITU_id]
        
        #pass band, block band frequency value
        self._ITU_freq_pass_R_val = self._ITU_freq_cen_val + self.sp_pass
        self._ITU_freq_pass_L_val = self._ITU_freq_cen_val - self.sp_pass
        
        self._ITU_freq_block_R_val = self._ITU_freq_cen_val + self.sp_block
        self._ITU_freq_block_L_val = self._ITU_freq_cen_val - self.sp_block 
        
        #Grid frequency value
        self._ITU_freq_grid_R_val = self._ITU_freq_cen_val + self.sp_grid
        self._ITU_freq_grid_L_val = self._ITU_freq_cen_val - self.sp_grid

        
        #Pass trace and Block trace
        if np.mod(self._ITU_id,2)==1:
            pass_data = even_data.copy()
            block_data = odd_data.copy()
        else:
            pass_data = odd_data.copy()
            block_data = even_data.copy()
        
        #Pass/block data sperate
        self.pass_wav = pass_data[0:,wav]
        self.block_wav = block_data[0:,wav]
        
        self.pass_freq = pass_data[0:,freq]
        self.block_freq = block_data[0:,freq]
        
        self.pass_GD = pass_data[0:,gd]
        self.block_GD = block_data[0:,gd]        
        
        self.pass_PDL = pass_data[0:,pdl]
        self.block_PDL = block_data[0:,pdl]        
        
        self.pass_PMD = pass_data[0:,pmd]
        self.block_PMD = block_data[0:,pmd]        
        
        self.pass_max_Loss = pass_data[0:,mxlos]
        self.block_max_Loss = block_data[0:,mxlos]
        
        self.pass_min_Loss = pass_data[0:,mnlos]
        self.block_min_Loss = block_data[0:,mnlos] 
        
        self.pass_IL = 0.5*(self.pass_max_Loss + self.pass_min_Loss)
        self.block_IL = 0.5*(self.block_max_Loss + self.block_min_Loss)
        
        self._ITU_freq_cen_idx = self.find_nearest_index(self.pass_freq, self._ITU_freq_cen_val)
        self._ITU_freq_pass_L_idx = self.find_nearest_index(self.pass_freq, self._ITU_freq_pass_R_val)
        self._ITU_freq_pass_R_idx = self.find_nearest_index(self.pass_freq, self._ITU_freq_pass_L_val)
        self._ITU_freq_block_L_idx = self.find_nearest_index(self.block_freq, self._ITU_freq_block_R_val)
        self._ITU_freq_block_R_idx = self.find_nearest_index(self.block_freq, self._ITU_freq_block_L_val)
        self._ITU_freq_grid_L_idx = self.find_nearest_index(self.pass_freq, self._ITU_freq_grid_R_val)
        self._ITU_freq_grid_R_idx = self.find_nearest_index(self.pass_freq, self._ITU_freq_grid_L_val)
            
        self._ITU_IL_pass_val = self.pass_IL[self._ITU_freq_cen_idx]
        
       
            
    def channel_parameter(self):
        '''
        channel ID, center frequency, center wavelength of current channel
        freq, unit in THz
        wavelength, unit in nm
        '''
        chn = self._ITU_id
        center_freq = self._ITU_freq_cen_val/1E3
        center_wavelength = self._ITU_wave_cen_val
        
        return chn, center_freq, center_wavelength        
        
    def IL(self):
        '''
        Insertion loss of passband
        '''
        
        
        IL_pass_cen = self._ITU_IL_pass_val
        IL_pass_worst_case = np.min(self.pass_max_Loss[self._ITU_freq_pass_L_idx : self._ITU_freq_pass_R_idx])
        IL_pass_best_case = np.max(self.pass_min_Loss[self._ITU_freq_pass_L_idx: self._ITU_freq_pass_R_idx])
        IL_ripple =np.abs( IL_pass_worst_case - IL_pass_best_case)
        
        IL_block_cen = self.block_IL[self._ITU_freq_cen_idx]
        IL_block_worst_cass = np.min(self.block_max_Loss[self._ITU_freq_pass_L_idx : self._ITU_freq_pass_R_idx])
        IL_block_best_case = np.max(self.block_min_Loss[self._ITU_freq_pass_L_idx: self._ITU_freq_pass_R_idx])
        
        
        return IL_pass_cen, IL_pass_best_case, IL_pass_worst_case, IL_ripple, IL_block_cen, IL_block_best_case, IL_block_worst_cass
    
    def passband(self,xdB = 0):
        '''
        get 0.5/1/3 dB passband and clear channel passband, return a tuple
        '''
        freq_L_idx = self.find_nearest_index(self.pass_IL[self._ITU_freq_grid_L_idx:self._ITU_freq_cen_idx+1], self._ITU_IL_pass_val - xdB) + self._ITU_freq_grid_L_idx
        freq_R_idx = self.find_nearest_index(self.pass_IL[self._ITU_freq_cen_idx:self._ITU_freq_grid_R_idx+1], self._ITU_IL_pass_val - xdB) + self._ITU_freq_cen_idx
        
        freq_L_val = self.pass_freq[freq_R_idx]
        freq_R_val = self.pass_freq[freq_L_idx]
        
        ccp_band_L = np.abs(self._ITU_freq_cen_val - freq_L_val)
        ccp_band_R = np.abs(freq_R_val - self._ITU_freq_cen_val)
        
        xdB_passband = np.abs(self.pass_freq[freq_L_idx] - self.pass_freq[freq_R_idx])
        xdB_ccp_passband = 2*np.min([ccp_band_L, ccp_band_R])
        xdB_wave_accuracy = 0.5*(ccp_band_R - ccp_band_L)
        
        return freq_L_idx, freq_R_idx, freq_L_val, freq_R_val, ccp_band_L,ccp_band_R, xdB_passband, xdB_ccp_passband, xdB_wave_accuracy

    def gdr_cd(self, order = 2):
        '''
        Under discussion.
        '''
        wave_list = self.pass_wav[self._ITU_freq_pass_L_idx : (self._ITU_freq_pass_R_idx+1)]
        wave_list_poly = wave_list - self._ITU_wave_cen_val
        gd_list = self.pass_GD[self._ITU_freq_pass_L_idx : (self._ITU_freq_pass_R_idx+1)] 
        
        polynomial = np.polyfit(wave_list_poly, gd_list, order)
        p1 = np.poly1d(polynomial)
        gd_list_poly = p1(wave_list_poly)
        
        
        gdr_list = gd_list - gd_list_poly
        gdr = gdr_list[np.abs(gdr_list).argmax()]
        
#        pl.plot(wave_list, gd_list, label='Init'),pl.plot(wave_list, gd_list_poly, label = 'Fit')
#        pl.show()
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
        polarization mode dispeersion, within SOP.
        Polarization mode dispersion (PMD), or differential group delay (DGD), is the 
        maximum difference in group delay over all polarization states.
        '''
#        pmd_max = np.max(self.pass_GD[self._ITU_freq_pass_L_idx : self._ITU_freq_pass_R_idx])
#        pmd_min = np.min(self.pass_GD[self._ITU_freq_pass_L_idx : self._ITU_freq_pass_R_idx])
        
        pmd_pmd = np.max(self.pass_PMD[self._ITU_freq_pass_L_idx : self._ITU_freq_pass_R_idx])
        
        
        return pmd_pmd
    
    @property
    def pdl(self):
        '''
        Polarization dependent loss, within SP.
        '''
        pdl = np.max(self.pass_PDL[self._ITU_freq_pass_L_idx : self._ITU_freq_pass_R_idx])
        return pdl    
    
    @property
    def ER(self):
        pass_min = np.min(self.pass_max_Loss[self._ITU_freq_pass_L_idx : (self._ITU_freq_pass_R_idx+1)])
        block_max = np.max(self.block_min_Loss[self._ITU_freq_block_L_idx : (self._ITU_freq_block_R_idx + 1)])
        
        return pass_min - block_max
        
    def make_wave(self, x=0, y = 0):
        '''
        make wave
        Xaxis, 0: wavelength, 1: frquencvy
        Yaxis, 0: IL, 1: GD, 2 :PDL, 3: PMD
        '''
        
        if x==0:
            xlabel = 'Wavelength (nm)'
            xaxis = self.pass_wav[self._ITU_freq_pass_L_idx: (self._ITU_freq_pass_R_idx+1)]
        elif x==1:
            xlabel = 'Frequency (THz)'
            xaxis = self.pass_freq[self._ITU_freq_pass_L_idx: (self._ITU_freq_pass_R_idx+1)]/1000
        else:
            raise NameError
        
        if y==0:
            ylable = "IL (dB)"
            yaxis = self.pass_IL[self._ITU_freq_pass_L_idx: (self._ITU_freq_pass_R_idx+1)]
        elif y==1:
            ylable = "GD (ps)"
            yaxis = self.pass_GD[self._ITU_freq_pass_L_idx: (self._ITU_freq_pass_R_idx+1)]
        elif y==2:
            ylable = "PDL (dB)"
            yaxis = self.pass_PDL[self._ITU_freq_pass_L_idx: (self._ITU_freq_pass_R_idx+1)]
        elif y==3:
            ylable = "PMD (ps)"
            yaxis = self.pass_PMD[self._ITU_freq_pass_L_idx: (self._ITU_freq_pass_R_idx+1)]
        else:
            raise NameError
        
        pl.plot(xaxis, yaxis, '.')
        pl.title(ylable)
        pl.xlabel(xlabel)
        pl.ylabel(ylable)
        pl.show()         
        
        
    def find_nearest_index(self,array,value):
        '''
        find the nearest value index in an array
        '''
        index = (np.abs(array - value)).argmin()
        return index        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        