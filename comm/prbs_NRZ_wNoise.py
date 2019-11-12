# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 22:23:09 2019

@author: Luna
"""

from comm_basic import *
#from commpy.filters import rrcosfilter

pattern_length = 200
prbs_type_1 = 31
prbs_type_2 = 13
Ts = 101
edge = 0.3
fsz = (8,5)



seq1 = PRBS_gen(prbs_type_1, pattern_length)
seq2 = gen_pulse(seq1, Ts)

p_shape = pulse_shape(1,0, 0,int(Ts*edge),int(Ts*edge), 0, int(Ts*(1+edge)))
final_1 = np.convolve(seq2, p_shape)

pwr_d_temp_seq = np.sum(abs(final_1)**2) # divide by time.  E/T

snr = 21.5#dB
snr_d = 10**(snr/10)
print('SNR is ',snr_d)

pwr_d_noise = pwr_d_temp_seq/snr_d
print('Noise power',pwr_d_noise)

sigma = np.sqrt(pwr_d_noise)
print('sigma is',sigma)

noise = Noise_gen(len(final_1),sigma)

final_2 = final_1 + noise


plot_eye(final_2, Ts, 0)
#plot_spectrum(final_1, 2*Ts, 'NRZ')










