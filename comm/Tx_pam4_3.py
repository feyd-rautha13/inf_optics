# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 15:57:13 2019

@author: Luna
"""

from transmitter2 import Transmitter
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np

n=1
baudrate = 1
run_point = 10000*n
samples = 2**5+1

#
#snr = 10


#-3 instance
tr_x = Transmitter(baudrate,run_point,samples)
#sequence
s0 = tr_x.genPRBS(7, 20)
'''
plt.stem(s0)
'''

#-2 encoder
#grey_seq = tr_x.genGreySerial(s0,2**n)
grey_seq = np.array([1,0,1,0,1,0,1,0,1,0])
'''
plt.stem(grey_seq)
'''

#grey_seq = tr_x.genGrey(s0,s1)

#-1 pulse shapiping time domain
xt_pshape, amp_pshape = tr_x.pulseShape(1,0, 0.1,0.1,samples, tr_x.ts)
'''
plt.plot(amp_pshape)
'''
#0 impulse generation time domain
xt_grey_impulse, amp_grey_impulse = tr_x.genImpuls(grey_seq, tr_x.sample_num, tr_x.ts)
rdt = np.diff(amp_grey_impulse)
rdit = np.cumsum(rdt)
'''
plt.plot(amp_grey_impulse)
plt.plot(rdt)
plt.plot(rdit)
'''

#1 waveform generate time domain
xt_pam, wav_pam = tr_x.genWavform(amp_grey_impulse, amp_pshape, tr_x.ts)



'''
plt.figure(figsize=(8,5))
amp1 = np.zeros(19)
amp2 = np.concatenate((amp1,amp_grey_impulse))
plt.stem(amp2, use_line_collection=True)
plt.plot(wav_pam, 'r')

'''
#for i in np.arange(1,30,1):
#
#    #2 waveform with noise generate
#    xt_pam_noz, wav_pam_noz = tr_x.genWaveWithNoise(wav_pam, i, tr_x.ts)
#    
#    #3 match filter
#    xt_match, amp_match_filter = tr_x.matchFilter(amp_pshape, tr_x.ts)
#    
#    #4 seq pass match filter from step 2
#    xt_r_wav, amp_r_wav = tr_x.genRxWaveform(wav_pam_noz, amp_match_filter, tr_x.ts)
#    
#    sample_r = tr_x.sampleRx(amp_r_wav, samples, 66)
#    decision_out = tr_x.decisionNRzRx(sample_r, 0.50)
#   
#    ber = tr_x.BERcount(grey_seq, decision_out)
#    print (ber)





