# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 15:57:13 2019

@author: Luna
"""

from transmitter import Transmitter
import matplotlib.pyplot as plt

baudrate = 2E9
run_point = 3E3
samples = 2**5+1


snr = 31
n=2


# instance
tr_x = Transmitter(baudrate,run_point,samples)
#sequence
s0 = tr_x.genPRBS(31, run_point)

#encoder
grey_seq = tr_x.genGreySerial(s0,2**n)
#grey_seq = tr_x.genGrey(s0,s1)

#pulse shapiping time domain
xt_pshape, amp_pshape = tr_x.pulseShape(1,0, 0.4,0.4,tr_x.sample_num, tr_x.ts)

#impulse generation time domain
xt_grey_impulse, amp_grey_impulse = tr_x.genImpuls(grey_seq, tr_x.sample_num, tr_x.ts)

#plt.figure(figsize=(8,5))
#plt.stem(amp_grey_impulse)

#waveform generate time domain
xt_pam, wav_pam = tr_x.genWavform(amp_grey_impulse, amp_pshape, tr_x.ts)

#waveform with noise generate
xt_pam_noz, wav_pam_noz = tr_x.genWaveWithNoise(wav_pam, snr, tr_x.ts)

# spectrum generation
x_fpam, f_amp_pam = tr_x.genSpectrum(wav_pam_noz, tr_x.ts)
'''
plt.figure(figsize=(8,5))
plt.plot(x_fpam[x_fpam<=(2*tr_x.baudrate+1)], f_amp_pam[x_fpam<=(2*tr_x.baudrate+1)])
plt.title("spectrum")
plt.show()
'''
# clock generation
x_f_clock, f_amp_clock = tr_x.genCDRspectrum(wav_pam_noz, tr_x.ts)

'''
plt.figure(figsize=(8,5))
plt.plot(x_f_clock[x_f_clock<=(2*tr_x.baudrate+1)], f_amp_clock[x_f_clock<=(2*tr_x.baudrate+1)])
plt.title("Clock")
plt.show()

# plot eye
tr_x.plot_eye(wav_pam, len(amp_pshape), tr_x.sample_num, 0,tr_x.ts)
tr_x.plot_eye(wav_pam_noz, len(amp_pshape), tr_x.sample_num, 0,tr_x.ts)
'''
