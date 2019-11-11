# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 22:23:09 2019

@author: Luna
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
from comm_basic import *
#from commpy.filters import rrcosfilter

pattern_length = 200
prbs_type_1 = 31
prbs_type_2 = 13
Ts = 101
edge = 0.3
fsz = (8,5)

#PRBS pattern sequence generation
def PRBS_gen(prbstype, pattern_length):
    pg_seq = sig.max_len_seq(nbits=prbstype, length=pattern_length)[0]
    
    return pg_seq

#Grey encoding
def encoder_grey(data):
    grey = {'00':0, '01':1, '11':2, '10':3}
    data_len = int(len(data[0]))
    grey_output = []
    for i in np.arange(data_len):
        stin = str(data[:,i][0])+str(data[:,i][1])
        grey_output.append(grey[stin])
    grey_output = [x/3 for x in grey_output]
    
    return grey_output

#pluse generation
def gen_pulse(seq, Ts):
    a1 = int((Ts-1)/2)
    allzero = np.zeros((a1,len(seq)))
    matrix1 = np.vstack((allzero,seq, allzero))
    matrix2 = np.reshape(matrix1, -1, order='F')
    
    return matrix2
    

# Pulse shape
def pulse_shape(high, low, pre_z, pre_raise, post_fall, post_z, total):
    pre_zero = np.zeros(pre_z)
    post_zero = np.zeros(post_z)
    pre_part = np.linspace(low,high,pre_raise)
    post_part = np.linspace(high,low,post_fall)
    mid = high*np.ones(total - pre_z - pre_raise - post_fall- post_z) 
    
    return np.concatenate((pre_zero,pre_part,mid,post_part, post_zero ))

#show eye
def plot_eye(data, Ts, offset):
    plt.figure(figsize=fsz)
    x_range = int((len(data) - Ts + 1)/Ts)
   
    for i in np.arange(x_range-1):
        try:
            plt.plot(data[(offset+2*Ts*i):(offset+2*Ts*(i+1))])
        except:
            pass
    plt.title('PAM4 EYE')
    plt.show()
    
def plot_eye2(data, Ts, offset):
    plt.figure(figsize=fsz)
    x_range = int((len(data) - Ts + 1)/Ts)
   
    for i in np.arange(x_range-1):
        try:
            plt.scatter(np.arange(2*Ts),data[(offset+2*Ts*i):(offset+2*Ts*(i+1))], alpha=0.7)
        except:
            pass
    plt.title('PAM4 EYE')
    plt.show()

def plot_spectrum(data, Ts, title):
    plt.figure(figsize=fsz)
    zz = 20*np.log10(np.fft.fft(data))
    plt.plot(zz[:Ts])
    plt.title('{0} Specturm'.format(title))
    plt.show()


pg_seq_N = PRBS_gen(prbs_type_1, pattern_length)
pg_seq_P = PRBS_gen(prbs_type_2, pattern_length)
pg_seq = np.vstack((pg_seq_N,pg_seq_P))
pam_seq = encoder_grey(pg_seq) 

pam_seq_pulse = gen_pulse(pam_seq, Ts)

p_shape = pulse_shape(1,0, 0,int(Ts*edge),int(Ts*edge), 0, int(Ts*(1+edge)))

temp_seq = np.convolve(pam_seq_pulse, p_shape)

pwr_d_temp_seq = np.sum(abs(temp_seq)**2)

snr = 30#dB
snr_d = 10**(snr/10)
print('SNR is ',snr_d)

pwr_d_noise = pwr_d_temp_seq/snr_d
print('Noise power',pwr_d_noise)

sigma = np.sqrt(pwr_d_noise/snr_d)
print('sigma is',sigma)


noise = Noise_gen(len(temp_seq),sigma)
 

temp_seq_1 = temp_seq + noise

plot_eye(temp_seq_1, Ts, 0)
plot_eye2(temp_seq_1, Ts, 0)

#plot_spectrum(temp_seq_1, Ts, 'PAM4')









