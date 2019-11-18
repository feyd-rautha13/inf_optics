# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 15:57:13 2019

@author: Luna
"""

from transmitter2 import Transmitter
import matplotlib.pyplot as plt
from scipy import signal

n=1
baudrate = 1.25E9
run_point = 1000*n
samples = 2**5+1


snr = 30


#-3 instance
tr_x = Transmitter(baudrate,run_point,samples)
#sequence
s0 = tr_x.genPRBS(7, run_point)

#-2 encoder
grey_seq = tr_x.genGreySerial(s0,2**n)
'''
plt.plot(grey_seq[:100])
plt.plot(grey_seq[9900:])
'''

#grey_seq = tr_x.genGrey(s0,s1)

#-1 pulse shapiping time domain
xt_pshape, amp_pshape = tr_x.pulseShape(1,0, 0.25,0.25,33, tr_x.ts)
'''
plt.plot(amp_pshape)
'''
#0 impulse generation time domain
xt_grey_impulse, amp_grey_impulse = tr_x.genImpuls(grey_seq, tr_x.sample_num, tr_x.ts)

#1 waveform generate time domain
xt_pam, wav_pam = tr_x.genWavform(amp_grey_impulse, amp_pshape, tr_x.ts)


'''
plt.plot(wav_pam[:2000])
plt.plot(wav_pam[200:400],'o')
'''

#2 waveform with noise generate
xt_pam_noz, wav_pam_noz = tr_x.genWaveWithNoise(wav_pam, snr, tr_x.ts)
'''
plt.plot(wav_pam_noz[:99])
'''

# spectrum generation
x_fpam, f_amp_pam = tr_x.genSpectrum(wav_pam_noz, tr_x.ts)
'''
plt.figure(figsize=(8,5))
plt.plot(x_fpam[x_fpam<=(2*tr_x.baudrate+1)], f_amp_pam[x_fpam<=(2*tr_x.baudrate+1)])
plt.title("spectrum")
plt.show()
'''

'''

# plot eye
tr_x.plot_eye(wav_pam, len(amp_pshape), tr_x.sample_num, 0,tr_x.ts)
tr_x.plot_eye(wav_pam_noz, len(amp_pshape), tr_x.sample_num, 0,tr_x.ts)
'''

#3 match filter
xt_match, amp_match_filter = tr_x.matchFilter(amp_pshape, tr_x.ts)
'''
plt.plot(amp_match_filter)
'''
#4 seq pass match filter from step 2
xt_r_wav, amp_r_wav = tr_x.genRxWaveform(wav_pam_noz, amp_match_filter, tr_x.ts)
'''
plt.plot(amp_r_wav[:99])
'''
# clock generation
#x_f_clock, f_amp_clock = tr_x.genCDRspectrum(wav_pam_noz, tr_x.ts)

'''
plt.figure(figsize=(8,5))
plt.plot(x_f_clock[x_f_clock<=(5*tr_x.baudrate+1)], f_amp_clock[x_f_clock<=(5*tr_x.baudrate+1)])
plt.title("Clock")
plt.show()
'''

# sample

sample_r = tr_x.sampleRx(amp_r_wav, samples, 66)
#decision_out = tr_x.decisionNRzRx(sample_r, 0.50)
'''
plt.plot(grey_seq[:100])
plt.plot(sample_r[:100])
plt.plot(decision_out[:100])
'''

#ber = tr_x.BERcount(grey_seq, decision_out)


    





