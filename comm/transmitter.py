# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 09:42:16 2019

@author: sliu3
"""
import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt

class Transmitter():
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

#        self.ts = 1/(self.baudrate*(self.sample_num-1))
        self.ts = 1/(self.baudrate*self.sample_num)
#        self.fs = self.baudrate*(sample_num-1)
        self.fs = self.baudrate*sample_num

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
        generate impuls
        return with sampling points
        '''
       
        a0 = int((sample_num-1)/2)
        allzeros = np.zeros((a0, len(seq)))
        pulse_matrix = np.vstack((allzeros, seq, allzeros)).reshape((-1), order='F')
        t_axis = ts*np.arange(len(pulse_matrix))
        
        
        return t_axis, pulse_matrix
    
        
        
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
    
    def plot_eye(self, seq, len_shape, sample_num, offset, ts=1):
        plt.figure(1, figsize=(8,5))
        cycle = int(((len(seq) - len_shape + 1)/sample_num/2)) #baudrate * trans_time/2
        step_num = 2*sample_num  
        t_axis = ts*np.arange(step_num+1)
        for i in np.arange(cycle):
            try:
                plt.plot(t_axis,seq[(offset+i*step_num):(offset+(i+1)*step_num+1)])
            except:
                pass
        
        plt.title("Eye Diagram")
        plt.show()
        
    def genSpectrum(self, seq, ts=1):
        amp = 20*np.log10(np.abs(np.fft.fft(seq)))
        amp = np.fft.fftshift(amp)
        f_xaxis = np.fft.fftfreq(len(amp),ts)
        f_xaxis = np.fft.fftshift(f_xaxis)

        return f_xaxis[f_xaxis>=0], amp[f_xaxis>=0]
    
    def genCDRspectrum(self,seq, ts=1):
        amp = np.square(np.abs(seq))
        amp = 20*np.log10(np.abs(np.fft.fft(amp)))
#        amp = np.fft.fftshift(amp)
        f_xaxis = np.fft.fftfreq(len(amp),ts)
#        f_xaxis = np.fft.fftshift(f_xaxis)
 
        return f_xaxis[f_xaxis>=0], amp[f_xaxis>=0]
        
        
        
        
       












