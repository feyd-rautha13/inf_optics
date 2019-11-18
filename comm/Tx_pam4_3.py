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
baudrate = 25.78125E9
run_point = 10000*n
samples = 2**5+1


snr = 10



#-3 instance
tr_x = Transmitter(baudrate,run_point,samples)
#sequence
s0 = tr_x.genPRBS(31, run_point)

#-2 encoder
grey_seq = tr_x.genGreySerial(s0,2**n)
'''
plt.plot(grey_seq[:100])
plt.plot(grey_seq[900:])
'''

#grey_seq = tr_x.genGrey(s0,s1)

#-1 pulse shapiping time domain
xt_pshape, amp_pshape = tr_x.pulseShape(1,0, 0.25,0.25,tr_x.sample_num, tr_x.ts)
'''
plt.plot(amp_pshape)
'''
#0 impulse generation time domain
xt_grey_impulse, amp_grey_impulse = tr_x.genImpuls(grey_seq, tr_x.sample_num, tr_x.ts)

#1 waveform generate time domain
xt_pam, wav_pam = tr_x.genWavform(amp_grey_impulse, amp_pshape, tr_x.ts)
wav_pam 

'''
plt.plot(wav_pam[:99])
plt.plot(wav_pam[32000:])
'''
for i in np.arange(1,30,1):

    #2 waveform with noise generate
    xt_pam_noz, wav_pam_noz = tr_x.genWaveWithNoise(wav_pam, i, tr_x.ts)
    
    
    #3 match filter
    xt_match, amp_match_filter = tr_x.matchFilter(amp_pshape, tr_x.ts)
    
    #4 seq pass match filter from step 2
    xt_r_wav, amp_r_wav = tr_x.genRxWaveform(wav_pam_noz, amp_match_filter, tr_x.ts)
    
    
    sample_r = tr_x.sampleRx(amp_r_wav, samples, 50)
    decision_out = tr_x.decisionNRzRx(sample_r, 0.50)
    
    
    ber = tr_x.BERcount(grey_seq, decision_out)
    print (ber)



#for j in np.arange(33,100,1):
#
#    #2 waveform with noise generate
#    xt_pam_noz, wav_pam_noz = tr_x.genWaveWithNoise(wav_pam, 30, tr_x.ts)
#    
#    
#    #3 match filter
#    xt_match, amp_match_filter = tr_x.matchFilter(amp_pshape, tr_x.ts)
#    
#    #4 seq pass match filter from step 2
#    xt_r_wav, amp_r_wav = tr_x.genRxWaveform(wav_pam_noz, amp_match_filter, tr_x.ts)
#    
#    
#    sample_r = tr_x.sampleRx(amp_r_wav, samples, j)
#    decision_out = tr_x.decisionNRzRx(sample_r, 0.50)
#    
#    
#    ber = tr_x.BERcount(grey_seq, decision_out)
#    print (j, ber)
#




