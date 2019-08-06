# -------------------------------------------------------------------------------
# Name:        OsaApex.py
# Purpose:
#
#
# Author:      Yingkan Chen
#
# Version:
#
# Created:     10/10/2016
# Copyright:   (c) Coriant R&D GmbH 2016
# -------------------------------------------------------------------------------

# System level import
import socket
import time
import math
import matplotlib.pyplot as plt
import numpy as np
from utility.retry import retry
from module.Prologix import Prologix
from scipy.signal import savgol_filter
from utility.pathmgr import pathmgr
from utility.toolkit import toolkit

c = 299792458.0


class Osa_hp86142a(Prologix):
    @retry(Exception, tries=20)
    def __init__(self, host='10.50.22.99', port=1234, addr="21", sock=None):
        Prologix.__init__(self, host, port, addr, sock)

        self.WLMIN = 600
        self.WLMAX = 1700
        self.FREQMIN = 176348
        self.FREQMAX = 499654

        print('%s initializing ... ' % self.getID().replace('\n', ''))

    def getID(self):
        '''
        Return string ID of AP2XXX equipment
        '''
        return self.ask("*IDN?\n")

    def setStartFrequency(self, frequency):
        if frequency < self.FREQMIN or frequency > self.FREQMAX:
            raise OverflowError("Given frequency is out of range")

        cmd = "sens:wav:star %dGHZ\n" % frequency
        self.write(cmd)
        time.sleep(5)

    def setStopFrequency(self, frequency):
        if frequency < self.FREQMIN or frequency > self.FREQMAX:
            raise OverflowError("Given frequency is out of range")

        cmd = "sens:wav:stop %dGHZ\n" % frequency
        self.write(cmd)
        time.sleep(5)

    def getStartFrequency(self):
        cmd = "sens:wav:star?\n"
        return c / float(self.ask(cmd)) / 1.0e9

    def getStopFrequency(self):
        cmd = "sens:wav:stop?\n"
        return c / float(self.ask(cmd)) / 1.0e9

    def setStartWavelength(self, Wavelength):
        '''
        Set the start wavelength of the measurement span
        Wavelength is expressed in nm
        '''
        if not isinstance(Wavelength, (float, int)):
            raise ValueError("Type of Wavelength is neither float nor int")

        if Wavelength < self.WLMIN or Wavelength > self.WLMAX:
            raise OverflowError("Given Wavelength is out of range")

        cmd = "sens:wav:star %.2fnm\n" % Wavelength
        self.write(cmd)
        time.sleep(5)

    def setStopWavelength(self, Wavelength):
        '''
        Set the stop wavelength of the measurement span
        Wavelength is expressed in nm
        '''
        if not isinstance(Wavelength, (float, int)):
            raise ValueError("Type of Wavelength is neither float nor int")

        if Wavelength < self.WLMIN or Wavelength > self.WLMAX:
            raise OverflowError("Given Wavelength in nm is out of range")

        cmd = "sens:wav:stop %.2fnm\n" % Wavelength
        self.write(cmd)
        time.sleep(5)

    def getStartWavelength(self):
        '''
        Get the start wavelength of the measurement span
        Wavelength is expressed in nm
        '''
        cmd = "sens:wav:star?\n"
        return float(self.ask(cmd))

    def getStopWavelength(self):
        '''
        Get the start wavelength of the measurement span
        Wavelength is expressed in nm
        '''
        cmd = "sens:wav:stop?\n"
        return float(self.ask(cmd))

    def setYMax(self, yRef):
        cmd = 'DISPlay:WINDow:TRACe:Y:SCALe:RLEVel %.2fDBM' % yRef
        self.write(cmd)

    def setSpanWL(self, Span):
        '''
        Set the wavelength measurement span
        Span is expressed in nm
        '''

        cmd = "SENS:WAV:SPAN %dnm\n" % Span
        self.write(cmd)

    def getSpanWL(self):
        '''
        Get the wavelength measurement span
        Span is expressed in nm
        '''
        cmd = "SENS:WAV:SPAN?\n"
        Span = self.ask(cmd)
        return float(Span[:-1]) * 1e9

    def setSpanFreq(self, Span):
        '''
        Set the wavelength measurement span
        Span is expressed in nm
        '''
        if not isinstance(Span, (float, int)):
            raise ValueError("Type of input Span is neither float nor int")

        cmd = "SENS:WAV:SPAN %dnm\n" % (Span / 12.5) * 0.1
        self.write(cmd)

    def getSpanFreq(self):
        '''
        Get the wavelength measurement span
        Span is expressed in nm
        '''
        cmd = "SENS:WAV:SPAN?\n"
        Span = self.ask(cmd)
        return float(Span[:-1]) * 1e9 / 0.1 * 12.5

    def setCenterWL(self, Center):
        '''
        Set the wavelength measurement center
        Center is expressed in nm
        '''

        Command = "SENS:WAV:CENT %.2fnm\n" % Center
        self.write(Command)

    def getCenterWL(self):
        '''
        Get the wavelength measurement center
        Center is expressed in nm
        '''
        Command = "SENS:WAV:CENT?\n"
        Center = self.ask(Command)
        return float(Center[:-1]) * 1e9

    def setCenterFreq(self, Center):
        '''
        Center in GHz
        Set the wavelength measurement center
        Center is expressed in nm
        '''

        Center = c / Center
        Command = "SENS:WAV:CENT %.2fnm\n" % Center
        self.write(Command)

    def getCenterFreq(self):
        '''
        Get the wavelength measurement center
        Center is expressed in nm
        '''
        Command = "SENS:WAV:CENT?\n"
        Center = self.ask(Command)
        return c / float(Center[:-1]) / 1e9

    def setXResolution(self, Resolution):
        '''
        Set the wavelength measurement resolution
        Resolution is expressed in the value of 'ScaleXUnit'
        'ScaleXUnit is either nm or GHz'
        '''
        Command = "sens:bwid:res %.2fnm\n" % Resolution
        self.write(Command)

    def getXResolution(self):
        '''
        Get the wavelength measurement resolution
        Resolution is expressed in the value of 'ScaleXUnit'
        '''
        Command = "sens:bwid:res?\n"
        XResolution = self.ask(Command)
        return float(XResolution[:-1])

    def setYResolution(self, Resolution):
        '''
        Set the Y-axis power per division value
        Resolution is expressed in the value of 'ScaleYUnit'
        'ScaleYUnit is either dB or mW'
        '''

        Command = "DISPlay:WINDow:TRACe:Y:SCALe:AUTO:PDIV %.2fDB\n" % Resolution
        self.write(Command)

    def getYResolution(self):
        '''
        Get the Y-axis power per division value
        Resolution is expressed in the value of 'ScaleYUnit'
        '''
        Command = "DISPlay:WINDow:TRACe:Y:SCALe:AUTO:PDIV?\n"
        YResolution = self.ask(Command)
        return float(YResolution[:-1])

    def runSweepMode(self, SweepMode):
        if SweepMode.lower() == 'auto':
            self.write('INIT:CONT on')
        elif SweepMode.lower() == 'single':
            self.write('SENSe:BANDwidth:VIDeo 1KHz')
            self.write('init:imm;*opc?')
            self.write('Temp')
            time.sleep(1)
        elif SweepMode.lower() == 'repeat':
            self.write('INIT:CONT on')
        elif SweepMode.lower() == 'stop':
            self.write('INIT:CONT off')

    def sweep(self):
        self.runSweepMode('single')

    def getOSNR(self):
        # self.runSweepMode('single')
        time.sleep(1)
        cmd = 'calc:mark1:func:osnr:state on'
        self.write(cmd)
        cmd = 'calc:mark1:func:osnr:res?'
        osnrValue = float(self.ask(cmd))
        print('Curr OSNR: %.2f dB' % osnrValue)
        return osnrValue

    def disconnect(self):
        self.sock.close()


if __name__ == "__main__":
    osa_inst = Osa_hp86142a()
    osa_inst.sweep()
    print(osa_inst.getOSNR())
    # print(osa_inst.getSpanFreq())
    # osa_inst.setStopWavelength(1551.91)
    # osa_inst.setStartWavelength(1549.91)
    # print(osa_inst.getStopFrequency())
    # osa_inst.setXResolution(0.5)
    # osa_inst.setYResolution(5)

    # osa_inst.setCenterWL(1550.910)
    # osa_inst.setSpanWL(4)
    # osa_inst.setXResolution(0.5)

    # print(osa_inst.getYResolution())
    # osa_inst.setYResolution(5)
    # osa_inst.runSweepMode('single')
    # osa_inst.setStopFrequency(193425)
    # osa_inst.setStartFrequency(193176)

    # print(osa_inst.ask('SPLINEVL?'))
    # print(osa_inst.ask('SPREFY?'))
    # x, y = osa_inst.measure(TraceNumber=1, NbAverage=1, centerFreq=193400, span = 100, plotFlag=True)
    # osa_inst.autoMeasure(TraceNumber=1, NbAverage=5, XDataScale='ghz', YDataScale='dB', sigBW=34)
    # osa_inst.autoMeasure(TraceNumber=1, NbAverage=5, XDataScale='nm', YDataScale='dB', sigBW=34)
    # y = osa_inst.getYLog(1)
    # x = osa_inst.getXFreq(1)
    # plt.plot(x,y)
    # plt.show()
    # peak = osa_inst.findPeak(TraceNumber=1, ThresholdValue=20.0)

    # toolkit.SaveWfm(pathmgr.data_tms_filter + 'Thomas_freq_qpsk_25_ndiff_0.8_core1.txt', freq)
    # toolkit.SaveWfm(pathmgr.data_tms_filter + 'Thomas_spec_qpsk_25_ndiff_0.8_core1.txt', spec)
    osa_inst.disconnect()
