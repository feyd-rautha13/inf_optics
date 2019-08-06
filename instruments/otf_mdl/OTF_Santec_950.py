#--------------------------------------------------------------------------------
# Name:        OTF_Santec_920.py
# Purpose:     
#              
#
# Author:      Yingkan Chen
#
# Version:     
#
# Created:     18/04/2017
# Copyright:   (c) Coriant R&D GmbH 2016
#-------------------------------------------------------------------------------
# Wavelength range: 1525 to 1565
# Freq range: 191.56 to 196.585
# System level import
import time
# site-package import

# 3rd party project module import

# Project module import
from module.otf_mdl.OTF import OTF

class OTF_Santec_950(OTF):
    def __init__(self, host = "10.50.22.102", port = 1234, addr = "28"):
        OTF.__init__(self, host, port, addr)

    def getWL(self):
        return self.ask(':WAV?')

    def setWL(self, wl_nm):
        self.write(':WAV %.3f' % wl_nm + 'nm')
        time.sleep(5)

    def setFreq(self, freq_THz):
        self.write(':FREQ %e' % int(freq_THz*1e12))
        print('Tuning OTF_950: %.5f THz' % freq_THz)
        while True:
            if abs(float(self.getFreq().split('\r')[0][1:]) - freq_THz*1e12)< 1e6:
                time.sleep(5)
                break
        print('Tuned OTF_950 to: %.5f THz' % freq_THz)

    def getFreq(self):
        return self.ask(':FREQ?')

    def getMinFreq(self):
        return self.ask(':WAV:MIN?')

    def getMaxFreq(self):
        return self.ask(':WAV:MAX?')

    def getBW(self):
        return self.ask(':BAND?')

    def setBW(self, bw):
        self.write(':BAND ' + str(bw) + 'nm')
        time.sleep(5)

if __name__ == "__main__":
    otf = OTF_Santec_950(host = "10.50.22.99", port = 1234, addr = "26")
    from module.voa_mdl.voa_agilent import voa_agilent

    # voa = voa_agilent(sock=otf.sock)

    print(otf.ask('*IDN?'))
    #
    print('current WL : %s' % otf.getWL())
    print('current Freq : %s' % otf.getFreq())
    print('current BW : %s' % otf.getBW())
    # print('Max Freq : %s' % otf.getMaxFreq())
    # print('Min Freq : %s' % otf.getMinFreq())
    #print(voa.ask('*IDN?'))
    otf.setBW(4)
    #print('current BW : %s' % otf.getBW())
    #

    otf.setFreq(193.4)
    print('current Freq : %s' % otf.getFreq())

    #
    # print('current Att: %s' % otf.getAtt())
    #
    # otf.setAtt(0.00)

    #otf.reset()

