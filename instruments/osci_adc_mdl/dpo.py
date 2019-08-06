# -------------------------------------------------------------------------------
# Name:        dpo.py
# Purpose:     
#              
#
# Author:      Yingkan Chen
#
# Version:     
#
# Created:     22/09/2016
# Copyright:   (c) Coriant R&D GmbH 2016
# -------------------------------------------------------------------------------

# System level import

# site-package import
import time
from struct import unpack

import matplotlib.pyplot as plt
import numpy as np
import visa

from utility.pathmgr import pathmgr
from utility.toolkit import toolkit


class dpo:
    def __init__(self, ip_addr="10.50.22.53", inst=0, recordLength=1e6):
        self.ip_addr_ = ip_addr
        self.rm_ = visa.ResourceManager()
        self.visaInst_ = inst
        self.recordLength = recordLength

        self.token_ = "TCPIP::" + self.ip_addr_ + "::inst" + str(self.visaInst_) + "::INSTR"
        self.dpo_inst_ = self.rm_.open_resource(self.token_, write_termination="\n")

        print(self.dpo_inst_.query('*IDN?') + " is connected")

        # initialization
        self.setDeviceClear()
        self.setHeader("off")
        self.setAcqSamplingMode("RT")
        self.setAcqMode("sample")
        self.setHorizontalModeRecordLength()

    def setDeviceClear(self):
        self.dpo_inst_.write("DeviceClear")

    def setHeader(self, cmd):
        self.dpo_inst_.write("header " + cmd)
        print("header is set to " + cmd)

    def setAcqSamplingMode(self, cmd):
        self.dpo_inst_.write("ACQuire:SAMPlingmode " + cmd)
        print("Sampling mode is set to " + cmd)

    def setAcqMode(self, cmd):
        '''SAMple specifies that the displayed data point value is the first sampled value
        that is taken during the acquisition interval. In sample mode, all waveform data
        has 8 bits of precision. You can request 16 bit data with a CURVe query but the
        lower-order 8 bits of data will be zero. SAMple is the default mode.'''
        self.dpo_inst_.write("ACQuire:MODe " + cmd)
        print("Acquire mode is set to " + cmd)

    def pressButtonRUNSTOP(self):
        self.setAcqRUN()
        self.setAcqOn()

    def pressButtonSingle(self):
        self.setAcqSingle()
        self.setAcqOn()

    def setAcqOn(self):
        self.dpo_inst_.write("ACQ:STATE ON")

    def setAcqOff(self):
        self.dpo_inst_.write("ACQUIR:STATE OFF")

    def setAcqRUN(self):
        self.dpo_inst_.write("ACQ:STOPA RUNST")

    def setAcqSingle(self):
        self.dpo_inst_.write("ACQ:STOPA SEQ")

    def setTriggerMode(self):
        self.dpo_inst_.write()

    def setHorizontalModeRecordLength(self):
        self.dpo_inst_.write('HORizontal:MODE:RECOrdlength ' + str(self.recordLength))

    def setHorizontalModeTimeDiv(self, time_div):
        self.dpo_inst_.write('HORizontal:MODE:SCAle ' + str(time_div))

    def setHorizontalModeSamplingRate(self, sampling_rate):
        self.dpo_inst_.write("HORizontal:MODE:SAMPLERate " + str(sampling_rate))

    def setHorizontalDelayMode(self, cmd):
        self.dpo_inst_.write("HORizontal:DELay:MODe " + cmd)
        print("Horizontal main delay mode is set to " + cmd)

    def setHorizontalDelayTime(self, hor_offset):
        self.dpo_inst_.write("HORizontal:DELay:TIMe " + str(hor_offset))

    def setAcqNumAvg(self, avg):
        self.dpo_inst_.write('ACQuire:NUMAVg ' + str(avg))

    def setHorizontalDelayPosition(self, refPos):
        self.dpo_inst_.write("HORizontal:DELay:POSition " + str(refPos))

    def setChannel(self, skew, bandwidth, ch_no):
        for ch_iter in ch_no:
            self.dpo_inst_.write("CH%d:DESKew " % skew(ch_iter))
            self.dpo_inst_.write('CH%d:BANdwidth:ENHanced AUTO' % ch_iter)
            self.dpo_inst_.write("CH%d:BANdwidth %d" % (ch_iter, bandwidth))

    def readWaveformFromScope(self, chNo):
        ''' 1. Select the waveform source(s) using DATa:SOUrce.
            2. Specify the waveform data format using DATa:ENCdg.
            3. Specify the number of bytes per data point using WFMOutpre:BYT_Nr.
                NOTE. MATH waveforms (and REF waveforms that came from a MATH) are
                always set to four bytes.
            4. Specify the portion of the waveform that you want to transfer using
                DATa:STARt and DATa:STOP.
            5. Transfer waveform preamble information using WFMOutpre.
            6. Transfer waveform data from the instrument using CURVe?.'''
        if (chNo > 5):
            print("WRONG CHANNEL NUMBER!!!")
            return

        self.dpo_inst_.write('DATA:SOU CH' + str(chNo))
        self.dpo_inst_.write('DATA:WIDTH 1')
        self.dpo_inst_.write('DATA:ENC RPB')
        self.dpo_inst_.write("DAT:STAR " + str(1))
        self.dpo_inst_.write("DAT:STOP " + str(self.recordLength))

        self.dpo_inst_.write("Curve?")

        # return value structure: #<x><yyy><data><\newline> (x is the number of bytes of yyy))'''
        data = self.dpo_inst_.read_raw()
        headerlen = int(data[1]) + 2
        ADC_wave = data[headerlen:-1]

        # B: unsigned char integer
        ADC_wave = np.array(unpack('%sB' % len(ADC_wave), ADC_wave))

        yoff = self.getVerticalOffset()
        ymult = self.getVerticalScale()
        yzero = self.getVerticalZero()
        xincr = self.getHorizontIncrement()

        volt = (ADC_wave - yoff) * ymult + yzero
        time = np.arange(0, xincr * len(volt), xincr)
        hdr = [len(ADC_wave), xincr, ymult, yoff]

        return volt, time, hdr

    def setWFMOutpreBinaryDataFormat(self, cmd="RI"):
        self.dpo_inst_.write("WFMOUTPRE:BN_FMT " + cmd)

    def closeSession(self):
        self.dpo_inst_.close()

    def getVerticalScale(self):
        return float(self.dpo_inst_.query("WFMOUTPRE:YMULT?"))

    def getVerticalOffset(self):
        '''This query-only command returns the vertical offset in digitized levels for the
            waveform specified by the DATa:SOUrce command'''
        return float(self.dpo_inst_.query("WFMOUTPRE:YOFF?"))

    def getVerticalZero(self):
        '''This query-only command returns the vertical offset in units specified by
        WFMOutpre:YUNit?'''
        return float(self.dpo_inst_.query("WFMOUTPRE:YZERO?"))

    def getVerticalUnit(self):
        '''This query-only command returns the vertical units for the waveform specified by
            the DATa:SOUrce command.'''
        return float(self.dpo_inst_.query("WFMOUTpre:YUNit?"))

    def getHorizontIncrement(self):
        return float(self.dpo_inst_.query("WFMPRE:XINCR?"))

    def getHorizontLength(self):
        return float(self.dpo_inst_.query(":HOR:RECORD?"))


if __name__ == "__main__":
    tekInst = dpo(ip_addr="10.50.22.53", inst=0, recordLength=1e6)
    tekInst.pressButtonRUNSTOP()
    time.sleep(2)
    tekInst.setAcqOff()
    time.sleep(2)
    tekInst.pressButtonSingle()
    time.sleep(2)
    volt1, time1, hdr1 = tekInst.readWaveformFromScope(1)
    volt2, time2, hdr2 = tekInst.readWaveformFromScope(2)
    volt3, time3, hdr3 = tekInst.readWaveformFromScope(3)
    volt4, time4, hdr4 = tekInst.readWaveformFromScope(4)

    plt.figure()
    plt.plot(time1, volt1, '-b')
    plt.figure()
    plt.plot(time2, volt2, '-r')
    plt.figure()
    plt.plot(time3, volt3, '-k')
    plt.figure()
    plt.plot(time4, volt4, '-m')
    plt.show()

    toolkit.saveWfm(pathmgr.datapath + "test_ch1.dat", volt1)
    toolkit.saveWfm(pathmgr.datapath + "test_ch1_hdr.dat", hdr1)
    toolkit.saveWfm(pathmgr.datapath + "test_ch2.dat", volt2)
    toolkit.saveWfm(pathmgr.datapath + "test_ch2_hdr.dat", hdr2)
    toolkit.saveWfm(pathmgr.datapath + "test_ch3.dat", volt3)
    toolkit.saveWfm(pathmgr.datapath + "test_ch3_hdr.dat", hdr3)
    toolkit.saveWfm(pathmgr.datapath + "test_ch4.dat", volt4)
    toolkit.saveWfm(pathmgr.datapath + "test_ch4_hdr.dat", hdr4)

    tekInst.closeSession()
