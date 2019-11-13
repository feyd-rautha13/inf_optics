# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 09:42:16 2019

@author: sliu3
"""
import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt

class transmitter():
    def __init__(self, BaudRate=1.25E9, tra_time= 0.001, sample_num = 33):
        '''
        Generate a sequence
        Baudrate symbol bandrate, unit symbol/s
        Tsym symbol period, unit s
        trans_time, similation time, unit s

        ts, sample time interval, unit second
        fs, sample frequency, unit Hz
        '''

        self.baudrate = BaudRate
        self.Tsym = 1/BaudRate
        self.trans_time = tra_time
        self.sample_num = sample_num

        self.ts = 1/(self.baudrate*(self.sample_num-1))
        self.fs = self.baudrate*(sample_num-1)

    def genPRBS(self, prbs_type, pattern_length):
        '''
        PRBS sequence generation
        '''
        seq = sig.max_len_seq(nbits=prbs_type, length = pattern_length)[0]

        return seq

    def genGrey(self, *seq):
        '''
        Grey code encoder
        multi paramters
        seq should be binary sequence 
        '''
        if len(seq) == 1:
            return seq[0]
        else:
            init = np.vstack((seq[0],seq[1]))
            try:
                for i in seq[2:]:
                    init = np.vstack((init, i))
            except:
                pass
            
            row,column = init.shape
            grey_code = []
            for i in np.arange(column):
                grey_binary = ''
                column_i = init[:,i]
                for j in column_i:
                    grey_binary += str(j)
                grey_code.append(grey_binary)
            grey_code = [int(i,2) for i in grey_code]
            grey_code = [(i^(i>>1)) for i in grey_code]
            return grey_code
    
    def genImpuls(self, seq, sample_num):
        '''
        return with sampling points
        '''
        a1 = int((sample_num-1)/2)
        allzero = np.zeros((a1,len(seq)))
        puls_matrix = np.vstack((allzero,seq,allzero)).reshape((-1), order='F')
        return puls_matrix
        
        
        
    def pulseShape(self,high,low,pre_z,post_z,raising,falling,total):
        pre_low = low*np.ones(pre_z)
        post_low = low*np.ones(post_z)
        raising_part = np.linspace(low,high,raising)
        falling_part = np.linspace(high,low,falling)
        mid = high*np.ones(total-pre_z-post_z-raising-falling)
        
        return np.concatenate((pre_low,raising_part,mid,falling_part,post_low))
    
    def genWavform(self,sequence, pulseShape, ts=1):
        '''
        Waveform generation, return time and amplitude
        '''
        amplitude = np.convolve(sequence, pulseShape)
        t_axis = ts*np.arange(len(amplitude))
        
        return t_axis,amplitude
    
    
        
# instance
tr_x = transmitter(1000,0.2,2**5+1)
#sequence
s0 = tr_x.genPRBS(31, 100)
s1 = tr_x.genPRBS(7,100)

#encoder
grey_seq = tr_x.genGrey(s0,s1)

#pulse shapiping
p_shape = tr_x.pulseShape(1,0.01,0,0,int(33*0.2),int(33*0.2),int(33*(1+0.2)))

#impulse generation
grey_impulse = tr_x.genImpuls(grey_seq,  tr_x.sample_num)

#waveform generate
wav_seq = tr_x.genWavform(grey_impulse, p_shape, tr_x.ts)


#fft
ffx = np.abs(np.fft.fft(wav_seq[1]))
ffx = 20*np.log10(np.abs(np.fft.fft(wav_seq[1])))
plt.plot(ffx)












