# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 15:28:27 2019

@author: Luna
"""

'''
NRZ
'''

from transmitter import Transmitter
import matplotlib.pyplot as plt

baudrate = 2E9
run_point = 3E3
samples = 2**5+1


snr = 31
n=1


tr = Transmitter(baudrate,run_point, samples)
# PRBS sequence
s0 = tr.genPRBS(31, run_point)
s1 = tr.genGreySerial(s0, 2**n)
# PRBS impluse
nrz_tx, nrz_pulse = tr.genImpuls(s1, samples, tr.ts)
#pulse shape
pshape_tx, pshape = tr.pulseShape(1,0,0.4,0.4,samples, tr.ts)
#PRBS waveform
nrz_w_tx, nrz_w = tr.genWavform(nrz_pulse, pshape, tr.ts)
#noise
nrz_w_n_tx, nrz_w_n = tr.genWaveWithNoise(nrz_w, snr, tr.ts)

#spectrum
nrz_fx, nrz_spec = tr.genSpectrum(nrz_w_n, tr.ts)
'''
plt.plot(nrz_fx[nrz_fx<=2*baudrate], nrz_spec[nrz_fx<=2*baudrate])
'''
#clock spectrum
nrz_c_fx, nrz_c_spec = tr.genCDRspectrum(nrz_w_n, tr.ts)
'''
plt.plot(nrz_c_fx[nrz_c_fx<=3*baudrate], nrz_c_spec[nrz_c_fx<=3*baudrate])
'''


'''
# eye
tr.plot_eye(nrz_w, len(pshape), tr.sample_num, 0,tr.ts)
tr.plot_eye(nrz_w_n, len(pshape), tr.sample_num, 0,tr.ts)
'''