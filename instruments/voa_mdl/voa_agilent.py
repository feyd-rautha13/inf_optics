# -------------------------------------------------------------------------------
# Name:        voa_agilent.py
# Purpose:
#
#
# Author:      Yingkan Chen
#
# Version:
#
# Created:     11/10/2016
# Copyright:   (c) Coriant R&D GmbH 2016
# -------------------------------------------------------------------------------

# System level import


# site-package import

# 3rd party project module import

# Project module import
from module.Prologix import Prologix


class voa_agilent(Prologix):
    def __init__(self, host = "10.50.22.102", port = 1234, addr = "20", sock = None):
        print('VOA Agilent initialing ... ')
        Prologix.__init__(self, host, port, addr, sock)

        if self.voaIsRunning:
            print('VOA Agilent is running.')

    def setWavelength(self, wav):
        self.write('INP1:WAV ' + str(wav) + 'nm')

    def set_att_value(self, dB):
        self.write('INP1:ATT %.2fdB' % dB)
        print(self.__class__.__name__ + ' is setting value to %.2f' % dB)

    def read_att_value(self):
        s = self.ask('INP1:ATT?')
        return float(s)
    # def setShutter(self):
    #     s = self.ask(':OUTP1:STAT?')
    #     # Check Shutter status
    #     if (int(s) == 0):
    #         print('Shutter was switched off -> Turn shutter on')
    #         s = self.write(':OUTP1:STAT ON')
    #     else:
    #         print('Shutter was switched on -> Turn shutter off')
    #         s = self.write(':OUTP1:STAT OFF')

    def setShutterOn(self):
        s = self.ask(':OUTP1:STAT?')
        # Check Shutter status
        if (int(s) == 0):
            print('Shutter was switched off -> Turn shutter on')
            s = self.write(':OUTP1:STAT ON')

    def setShutterOff(self):
        s = self.ask(':OUTP1:STAT?')
        # Check Shutter status
        if (int(s) == 1):
            print('Shutter was switched on -> Turn shutter off')
            s = self.write(':OUTP1:STAT OFF')


# ==============================================================================
if __name__ == '__main__':
    voa_inst = voa_agilent()
    #
    # #    # *IDN?
    cmd = "*IDN?"
    s = voa_inst.ask(cmd)
    print(s)
    # #
    # #    s = voa.ask(':SLOT1:IDN?')
    # #    print('slot1=', s
    # ##    s = voa.ask(':SLOT2:IDN?')
    # ##    print('slot2=', s
    #
    #
    # #############
    # # Read ATT
    # #############
    # s = voa_inst.ask('INP1:ATT?')
    # print('att=', s)
    #
    # #############
    # # Set ATT
    # #############
    # s = voa_inst.write('INP1:ATT 15.08dB')
    # print('att=', s)
    #
    # #############
    # # Read ATT
    # #############
    # s = voa_inst.ask('INP1:ATT?')
    # print('att=', s)
    #
    # #############
    # # Read Shutter status
    # #############
    # s = voa_inst.ask(':OUTP1:STAT?')
    # print('shutter=', s)
    #
    # #############
    # # Switch Shutter status
    # #############
    # if int(s):
    #     print('turn shutter off')
    #     s = voa_inst.write(':OUTP1:STAT OFF')
    # else:
    #     print('turn shutter on')
    #     s = voa_inst.write(':OUTP1:STAT ON')
    #
    # #############
    # # Read Shutter status again
    # #############
    # s = voa_inst.ask(':OUTP1:STAT?')
    # print('shutter=', s)
    # voa_inst.setShutterOn()
    # voa_inst.set_att_value(2)
    voa_inst.setShutterOff()
    voa_inst.closeConnection()
