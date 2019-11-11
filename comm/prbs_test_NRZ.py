# -*- coding: utf-8 -*-
"""r
Created on Sat Nov  9 22:23:09 2019

@author: Luna
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sig
#from commpy.filters import rrcosfilter

pattern_length = 200
prbs_type_1 = 31
prbs_type_2 = 13
Ts = 10001
edge = 0.2
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
    plt.title('eye')
    plt.show()

def plot_spectrum(data, Ts, title):
    plt.figure(figsize=fsz)
    zz = 20*np.log10(np.fft.fft(data))
    plt.plot(zz[:Ts])
    plt.title('{0} Specturm'.format(title))
    plt.show()

seq1 = PRBS_gen(prbs_type_1, pattern_length)
seq2 = gen_pulse(seq1, Ts)

p_shape = pulse_shape(1,0, 0,int(Ts*edge),int(Ts*edge), 0, int(Ts*(1+edge)))

final_1 = np.convolve(seq2, p_shape)

plot_eye(final_1, Ts, 0)
plot_spectrum(final_1, int(Ts/30), 'NRZ')










