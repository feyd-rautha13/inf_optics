# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 09:42:16 2019

@author: sliu3
"""
import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt

class transmitter():
    def __init__(self, BaudRate=1.25E9, trans_time= 0.001, sample_num = 33):
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
        self.trans_time = trans_time
        self.seq_num = BaudRate*trans_time
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
    
    def genImpuls(self, seq, sample_num, ts=1):
        '''
        return with sampling points
        '''
        a1 = int((sample_num-1)/2)
        allzero = np.zeros((a1,len(seq)))
        puls_matrix = np.vstack((allzero,seq,allzero)).reshape((-1), order='F')
        t_axis = ts*np.arange(len(puls_matrix))
        
        return t_axis, puls_matrix
    
        
        
    def pulseShape(self,high=1,low=0,raise_duty=0.15,fall_duty=0.15,sample_num=100,ts=1):
        '''
        high: level 1
        low: level 0
        rasie_duty: 0 <= raise_duty < 0.5
        fall_duty: 0<= fall duty < 0.5
        sample_num : equals to self.sample number
        '''
        raise_num = int(sample_num*raise_duty)
        fall_num = int(sample_num*fall_duty)
        total = sample_num + int(0.5*(raise_num + fall_num))
        
        raising_part = np.linspace(low,high,raise_num)
        falling_part = np.linspace(high,low,fall_num)
        mid = high*np.ones(total - raise_num - fall_num)
        
        
        amplitude = np.concatenate((raising_part,mid,falling_part))
        t_axis = ts*np.arange(len(amplitude))
       
        return t_axis, amplitude
    
    def genWavform(self,sequence, pulseShape, ts=1):
        '''
        Waveform generation, return time and amplitude
        '''
        amplitude = np.convolve(sequence, pulseShape)
        t_axis = ts*np.arange(len(amplitude))
        
        return t_axis,amplitude
    
    def genWaveWithNoise(self, seq, SNR, ts=1):
        '''
        SNR: logarithmic, unit dB.
        '''
        SNR = 10**(SNR/10)
        pwr_seq = np.sum(np.square(seq))/len(seq)
        
        pwr_noise = pwr_seq/SNR
        sigma = np.sqrt(pwr_noise)
        noise = np.random.normal(0, sigma, len(seq))
        wav = seq + noise
        t_axis = ts*np.arange(len(wav))
        
        return t_axis, wav
    
    def plot_eye(self, seq, shape_len, sample_num, offset, ts=1):
        plt.figure(1, figsize=(8,5))
        x_range = int((len(seq) - shape_len +1)/sample_num)
        
        t_axis = ts*np.arange(2*sample_num)
        
        for i in np.arange(x_range):
            try:
                plt.plot(t_axis,seq[(offset+2*sample_num*i):(offset+2*sample_num*(i+1))])
            except:
                pass
        plt.title("Eye Diagram")
        plt.show()
        
    def plot_spectrum(self, seq, ts=1):
        amp = 20*np.log10(np.abs(np.fft.fft(seq)))
        x_axis = np.fft.fftfreq(len(amp), ts)
        
        plt.figure(figsize=(8,5))
        plt.plot(x_axis[x_axis>=0], amp[x_axis>=0])
        plt.show()
    
    def CDR_spectrum(self,seq, ts=1):
        amp = np.square(seq)
        cdr = 20*np.log10(np.abs(np.fft.fft(amp)))
        x_axis = np.fft.fftfreq(len(amp), ts)
        
        plt.figure(figsize=(8,5))
        plt.plot(x_axis[x_axis>=0], cdr[x_axis>=0])
        plt.show()       
        
        
        
        
       
# instance
tr_x = transmitter(1E6,0.001,2**5+1)
#sequence
s0 = tr_x.genPRBS(31, tr_x.seq_num)
s1 = tr_x.genPRBS(7,tr_x.seq_num)

#encoder
grey_seq = tr_x.genGrey(s0,s1)

#pulse shapiping
xt_pshape, amp_pshape = tr_x.pulseShape(1,0, 0.2,0.2,tr_x.sample_num, tr_x.ts)

#impulse generation
xt_grey_impulse, amp_grey_impulse = tr_x.genImpuls(grey_seq, tr_x.sample_num, tr_x.ts)

#waveform generate
xt_pam, wav_pam = tr_x.genWavform(amp_grey_impulse, amp_pshape, tr_x.ts)

#waveform with noise generate
xt_pam_noz, wav_pam_noz = tr_x.genWaveWithNoise(wav_pam, 31, tr_x.ts)

tr_x.plot_eye(wav_pam_noz,len(amp_pshape), tr_x.sample_num, 0, tr_x.ts)
tr_x.plot_spectrum(wav_pam, tr_x.ts)
tr_x.CDR_spectrum(wav_pam, tr_x.ts)



