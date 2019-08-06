#-------------------------------------------------------------------------------
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

# System level import
import time
# site-package import

# 3rd party project module import

# Project module import
from module.otf_mdl.OTF import OTF

class OTF_Santec_920(OTF):
    def __init__(self, host, port, addr):
        OTF.__init__(self, host, port, addr)

    def getWL(self):
        return self.ask('WA?')

    def setWL(self, wl):
        self.write('WA %.3f' % wl)
        time.sleep(5)

    def getAtt(self):
        return self.ask('AT?')

    def setAtt(self, att):
        self.write('AT %.3f' % att)

    def reset(self):
        self.write('RE')

    def setSliderActive(self, activateList):
        for i in activateList:
            self.write('SE %d' % i)
            time.sleep(1)

    def setSliderFixed(self, fixedList):
        for i in fixedList:
            self.write('SD %d' % i)

    def setSliderOffset(self, offset_nm):
        self.write('DO %.3f' % offset_nm)
        time.sleep(3)

if __name__ == "__main__":
    otf = OTF_Santec_920(host = "10.50.22.102", port = 1234, addr = "3")
    print('current WL: %s' % otf.getWL())
    #otf.setWL(1554.5)
    #
    # print('changed to : %s' % otf.getWL())
    #
    # print('current Att: %s' % otf.getAtt())
    #
    # otf.setAtt(0.00)

    #otf.reset()

