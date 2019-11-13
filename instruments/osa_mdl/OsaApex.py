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
from scipy.signal import savgol_filter
from utility.pathmgr import pathmgr
from utility.toolkit import toolkit

class OsaApex:
    @retry(Exception, tries=20)
    def __init__(self, ipaddr='10.50.22.207', port=5900):

        self.host_ = ipaddr
        self.port_ = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(500)
        self.sock.connect((self.host_, self.port_))

        self.WLMIN = 1526
        self.WLMAX = 1566
        self.FREQMIN = 191570
        self.FREQMAX = 196456
        self.SPANMINWL = 0.08  # nm
        self.SPANMAXWL = 42  # nm
        self.SPANMINF = 10  # ghz
        self.SPANMAXF = 5250  # ghz

        self.RESMINWL = 0.00016  # nm
        self.RESMAXWL = 0.0008  # nm
        self.RESMINF = 0.02  # GHz
        self.RESMAXF = 0.1  # GHz

        print(self.getID())

    def getID(self):
        '''
        Return string ID of AP2XXX equipment
        '''
        return self.ask("*IDN?\n")

    def setStartFrequency(self, frequency):
        if frequency < self.FREQMIN or frequency > self.FREQMAX:
            raise OverflowError("Given frequency is out of range")

        cmd = "SPSTRTF" + str(frequency) + "\n"
        self.write(cmd)
        time.sleep(5)

    def setStopFrequency(self, frequency):
        if frequency < self.FREQMIN or frequency > self.FREQMAX:
            raise OverflowError("Given frequency is out of range")

        cmd = "SPSTOPF" + str(frequency) + "\n"
        self.write(cmd)
        time.sleep(5)

    def getStartFrequency(self):
        cmd = "SPSTRTF?\n"
        return float(self.ask(cmd))

    def getStopFrequency(self):
        cmd = "SPSTOPF?\n"
        return float(self.ask(cmd))

    def setStartWavelength(self, Wavelength):
        '''
        Set the start wavelength of the measurement span
        Wavelength is expressed in nm
        '''
        if not isinstance(Wavelength, (float, int)):
            raise ValueError("Type of Wavelength is neither float nor int")

        if Wavelength < self.WLMIN or Wavelength > self.WLMAX:
            raise OverflowError("Given Wavelength is out of range")

        cmd = "SPSTRTWL" + str(Wavelength) + "\n"
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

        cmd = "SPSTOPWL" + str(Wavelength) + "\n"
        self.write(cmd)
        time.sleep(5)

    def getStartWavelength(self):
        '''
        Get the start wavelength of the measurement span
        Wavelength is expressed in nm
        '''
        cmd = "SPSTRTWL?\n"
        return float(self.ask(cmd))

    def getStopWavelength(self):
        '''
        Get the start wavelength of the measurement span
        Wavelength is expressed in nm
        '''
        cmd = "SPSTOPWL?\n"
        return float(self.ask(cmd))

    def setYMax(self, yRef):
        cmd = 'SPREFY' + str(yRef)
        self.write(cmd)

    def setSpanWL(self, Span):
        '''
        Set the wavelength measurement span
        Span is expressed in nm
        '''
        if not isinstance(Span, (float, int)):
            raise ValueError("Type of input Span is neither float nor int")

        if Span < self.SPANMINWL or Span > self.SPANMAXWL:
            raise ValueError('Given Span in nm is out of range')

        cmd = "SPSPANWL" + str(Span) + "\n"
        self.write(cmd)

    def getSpanWL(self):
        '''
        Get the wavelength measurement span
        Span is expressed in nm
        '''
        cmd = "SPSPANWL?\n"
        Span = self.ask(cmd)
        return float(Span[:-1])

    def setSpanFreq(self, Span):
        '''
        Set the wavelength measurement span
        Span is expressed in nm
        '''
        if not isinstance(Span, (float, int)):
            raise ValueError("Type of input Span is neither float nor int")

        cmd = "SPSPANF" + str(Span) + "\n"
        self.write(cmd)

    def getSpanFreq(self):
        '''
        Get the wavelength measurement span
        Span is expressed in nm
        '''
        cmd = "SPSPANF?\n"
        Span = self.ask(cmd)
        return float(Span[:-1])

    def setCenterWL(self, Center):
        '''
        Set the wavelength measurement center
        Center is expressed in nm
        '''
        if not isinstance(Center, (float, int)):
            raise ValueError("Type of input Center is neither float nor int")

        if Center < self.WLMIN + self.SPANMINWL / 2 or Center > self.WLMAX - self.SPANMINWL / 2:
            raise ValueError('Given Center in nm is out of range')

        Command = "SPCTRWL" + str(Center) + "\n"
        self.write(Command)

    def getCenterWL(self):
        '''
        Get the wavelength measurement center
        Center is expressed in nm
        '''
        Command = "SPCTRWL?\n"
        Center = self.ask(Command)
        return float(Center[:-1])

    def setCenterFreq(self, Center):
        '''
        Set the wavelength measurement center
        Center is expressed in nm
        '''
        if not isinstance(Center, (float, int)):
            raise ValueError("Type of input Center is neither float nor int")

        if Center < self.FREQMIN + self.SPANMINF / 2 or Center > self.FREQMAX - self.SPANMINF / 2:
            raise ValueError('Given Center in nm is out of range')

        Command = "SPCTRF" + str(Center) + "\n"
        self.write(Command)

    def getCenterFreq(self):
        '''
        Get the wavelength measurement center
        Center is expressed in nm
        '''
        Command = "SPCTRF?\n"
        Center = self.ask(Command)
        return float(Center[:-1])

    def setXResolution(self, Resolution):
        '''
        Set the wavelength measurement resolution
        Resolution is expressed in the value of 'ScaleXUnit'
        'ScaleXUnit is either nm or GHz'
        '''
        Command = "SPSWPRES" + str(Resolution) + "\n"
        self.write(Command)

    def getXResolution(self):
        '''
        Get the wavelength measurement resolution
        Resolution is expressed in the value of 'ScaleXUnit'
        '''
        Command = "SPSWPRES?\n"
        XResolution = self.ask(Command)
        return float(XResolution[:-1])

    def setYResolution(self, Resolution):
        '''
        Set the Y-axis power per division value
        Resolution is expressed in the value of 'ScaleYUnit'
        'ScaleYUnit is either dB or mW'
        '''
        Command = "SPDIVY" + str(Resolution) + "\n"
        self.write(Command)

    def getYResolution(self):
        '''
        Get the Y-axis power per division value
        Resolution is expressed in the value of 'ScaleYUnit'
        '''
        Command = "SPDIVY?\n"
        YResolution = self.ask(Command)
        return float(YResolution[:-1])

    def setNPoints(self, NPoints):
        '''
        Set the number of points for the measurement
        '''
        if not isinstance(NPoints, int):
            raise ValueError('Type of input YResolution is not int')

        if NPoints < 2 or NPoints > 2e4:
            raise ValueError('Given NPoints is out of range')

        Command = "SPNBPTSWP" + str(NPoints) + "\n"
        self.write(Command)

    def getNPoints(self):
        '''
        Get the number of points for the measurement
        '''
        Command = "SPNBPTSWP?\n"
        NPoints = self.ask(Command)
        return int(NPoints[:-1])

    def runSweepMode(self, SweepMode):
        if SweepMode.lower() == 'auto':
            self.write('SPSWP0')
        elif SweepMode.lower() == 'single':
            time.sleep(.5)
            self.write('SPSWP1')
            self.sock.send("++read eoi\n")
            status = self.sock.recv(1000)
            return status
        elif SweepMode.lower() == 'repeat':
            self.write('SPSWP2')
        elif SweepMode.lower() == 'stop':
            self.write('SPSWP3')

    def getData(self, XScale='nm', YScale='dB', traceNum=1):
        if XScale.lower() == 'nm':
            XData = self.getXWavelength(traceNum)
        else:
            XData = self.getXFreq(traceNum)

        if YScale.lower() == 'db':
            YData = self.getYLog(traceNum)
        else:
            YData = self.getYLin(traceNum)

        return XData, YData

    def getYLog(self, traceNum):
        Npoint = self.getNPoints()
        cmd = 'SPDATAD' + str(traceNum)
        self.write(cmd)
        time.sleep(.5)
        self.sock.send("++read eoi\n")
        data = self.recvall()
        data = np.fromstring(data, sep=' ')
        return data[1:]

    def getYLin(self, traceNum):
        Npoint = self.getNPoints()
        cmd = 'SPDATAL' + str(traceNum)
        self.write(cmd)
        time.sleep(.5)
        self.sock.send("++read eoi\n")
        data = self.recvall()
        data = np.fromstring(data, sep=' ')
        return data[1:]

    def getXFreq(self, traceNum):
        Npoint = self.getNPoints()
        cmd = 'SPDATAF' + str(traceNum)
        self.write(cmd)
        time.sleep(.5)
        self.sock.send("++read eoi\n")
        data = self.recvall()
        data = np.fromstring(data, sep=' ')
        return data[1:]

    def getXWavelength(self, traceNum):
        Npoint = self.getNPoints()
        cmd = 'SPDATAWL' + str(traceNum)
        self.write(cmd)
        time.sleep(.5)
        self.sock.send("++read eoi\n")
        data = self.recvall()
        data = np.fromstring(data, sep=' ')
        return data[1:]

    def setNoiseMask(self, NoiseMaskValue):
        '''
        Set the noise mask of the signal (values under this mask are set to this value)
        Noise mask is expressed in the value of 'ScaleYUnit'
        '''
        if not isinstance(NoiseMaskValue, (float, int)):
            raise ValueError('Type of input NoiseMaskValue is neither float nor int')

        Command = "SPSWPMSK" + str(NoiseMaskValue) + "\n"
        self.write(Command)
        self.NoiseMaskValue = NoiseMaskValue

    def setScaleXUnit(self, ScaleXUnit='ghz'):
        '''
        Defines the unit of the X-Axis
        ScaleXUnit can be a string or an integer
        If ScaleXUnit is :
            - "ghz" or 0, X-Axis unit is in GHz (default)
            - "nm" or 1, X-Axis unit is in nm
        '''
        if isinstance(ScaleXUnit, str):
            if ScaleXUnit.lower() == "nm":
                ScaleXUnit = 1
            else:
                ScaleXUnit = 0

        Command = "SPXUNT" + str(ScaleXUnit) + "\n"
        self.write(Command)

        self.ScaleXUnit = ScaleXUnit

    def setScaleYUnit(self, ScaleYUnit='dB'):
        '''
        Defines the unit of the Y-Axis
        ScaleXUnit can be a string or an integer
        If ScaleYUnit is :
            - "lin" or 0, Y-Axis unit is in mW (default)
            - "log" or 1, Y-Axis unit is in dBm or dBm
        '''
        if isinstance(ScaleYUnit, str):
            if ScaleYUnit.lower() == "db":
                ScaleYUnit = 1
            else:
                ScaleYUnit = 0

        Command = "SPLINSC" + str(ScaleYUnit) + "\n"
        self.write(Command)
        self.ScaleYUnit = ScaleYUnit

    def setPolarizationMode(self, PolarizationMode):
        '''
        Defines the measured polarization channels
        PolarizationMode can be a string or an integer
        If PolarizationMode is :
            - "1+2" or 0, the total power is measured (default)
            - "1&2" or 1, one measure is done for each polarization channel
            - "1" or 2, just the polarization channel 1 is measured
            - "2" or 3, just the polarization channel 2 is measured
        '''
        if isinstance(PolarizationMode, str):
            if PolarizationMode.lower() == "1&2":
                PolarizationMode = 1
            elif PolarizationMode.lower() == "1":
                PolarizationMode = 2
            elif PolarizationMode.lower() == "2":
                PolarizationMode = 3
            else:
                PolarizationMode = 0

        Command = "SPPOLAR" + str(PolarizationMode) + "\n"
        self.write(Command)
        self.PolarizationMode = PolarizationMode

    def deleteAll(self):
        '''
        Clear all traces
        '''
        Command = "SPTRDELAL\n"
        self.write(Command)

    def lockTrace(self, traceNum):
        cmd = 'SPTRLOCK' + str(traceNum)
        self.write(cmd)

    def unlockTrace(self, traceNum):
        cmd = 'SPTRUNLOCK' + str(traceNum)
        self.write(cmd)

    def deleteTrace(self, traceNum):
        cmd = 'SPTRDEL' + str(traceNum)
        self.write(cmd)

    def activateAutoNPoints(self):
        '''
        Activates the automatic number of points for measurements
        '''

        Command = "SPAUTONBPT1\n"
        self.write(Command)

    def deactivateAutoNPoints(self):
        '''
        Deactivates the automatic number of points for measurements
        '''
        Command = "SPAUTONBPT0\n"
        self.write(Command)

    def findPeak(self, TraceNumber=1, ThresholdValue=20.0):
        '''
        Find the peaks in the selected trace
        TraceNumber is an integer between 1 (default) and 6
        ThresholdValue is a float expressed in dB (The difference between Peak and the noise level)
        '''
        Command = "SPPKFIND" + str(TraceNumber) + "_" + str(ThresholdValue) + "\n"
        self.write(Command)
        time.sleep(5)
        # Peak1 = Receive(self.Connexion)
        Command2 = "SPDATAMKRX" + str(TraceNumber) + "\n"
        self.write(Command2)
        Peak = self.recvall()
        return float(Peak.split(" ")[1])

    def activateAverageMode(self):
        '''
        Activates the average mode
        '''
        Command = "SPAVERAGE1\n"
        self.write(Command)

    def deactivateAverageMode(self):
        '''
        Deactivates the average mode
        '''
        Command = "SPAVERAGE0\n"
        self.write(Command)

    def wavelengthCalib(self):
        '''
        Performs a wavelength calibration.
        If a measurement is running, it is previously stopped
        '''

        Command = "SPWLCALM\n"
        self.write(Command)

    def setXmin2display(self, value):
        cmd = 'SPLINEVL' + str(int(value))
        self.write(cmd)

    def setXmax2display(self, value):
        cmd = 'SPLINEVR' + str(int(value))
        self.write(cmd)

    def setYmax2display(self, value):
        cmd = 'SPLINEHT' + str(int(value))
        self.write(cmd)

    def setYmin2display(self, value):
        cmd = 'SPLINEHB' + str(int(value))
        self.write(cmd)

    def setNpointAutoManual(self, mode='auto'):
        if mode.lower() == 'auto':
            cmd = 'SPAUTONBPT1'
        elif mode.lower() == 'manual':
            cmd = 'SPAUTONBPT0'
        self.write(cmd)

    def ask(self, cmd):
        self.write(cmd)
        time.sleep(.5)
        self.sock.send("++read eoi\n")
        return self.sock.recv(1000)

    def write(self, cmd):
        strtmp = cmd + "\n"
        self.sock.send(strtmp.encode())

    def disconnect(self):
        self.sock.close()

    def recvall(self):
        data = ""
        while True:
            part = self.sock.recv(4096)
            data += part
            tmp = np.fromstring(data, sep=' ')
            if not (len(tmp) < (tmp[0] + 1)):
                break
        return data

    def autoMeasure(self, TraceNumber=1, NbAverage=1, XDataScale='nm', YDataScale='dB', Npoint = None, sigBW=34, plotFlag = False):
        '''
        Auto measurement which performs a peak search
        and selects the spectral range and modify the span
        TraceNumber is an integer between 1 (default) and 6
        NbAverage is the number of average to perform after the span selection (no average by default)
        '''

        if int(NbAverage) < 1:
            NbAverage = 1

        if Npoint != None:
            self.setNpointAutoManual('manual')
            self.setNPoints(5000)

        self.deleteAll()

        self.setScaleXUnit(XDataScale)
        self.setScaleYUnit(YDataScale)

        if XDataScale.lower() == 'ghz':
            # set x range
            self.setStartFrequency(self.FREQMIN)
            self.setStopFrequency(self.FREQMAX)
            # set sweep resolution 100 MHz
            self.setXResolution(self.RESMAXF)

        elif (XDataScale.lower() == 'nm'):
            # set x range
            self.setStartWavelength(self.WLMIN)
            self.setStopWavelength(self.WLMAX)
            # set sweep resolution 80 nm
            self.setXResolution(self.RESMAXWL)

        print('Sweep over whole bandwidth supported by the OSA')
        self.runSweepMode("single")
        print('Sweep done')

        peak = self.findPeak(TraceNumber=TraceNumber, ThresholdValue=20.0)
        print('Peak is found at ' + str(peak))

        if XDataScale.lower() == 'ghz':
            spanF = sigBW * 2  # GHz
            self.setSpanFreq(spanF)
            self.setCenterFreq(peak)
            self.setStartFrequency(peak - spanF / 2)
            self.setStopFrequency(peak + spanF / 2)

        elif XDataScale.lower() == 'nm':
            spanWL = (sigBW * 2) / 12.5 * 0.1  # nm
            self.setSpanWL(spanWL)
            self.setCenterWL(peak)
            self.setStartWavelength(peak - spanWL / 2)
            self.setStopWavelength(peak + spanWL / 2)

        self.setNpointAutoManual('auto')

        self.avgMode(NbAverage=NbAverage)

        x, y = self.getData(XDataScale, YDataScale, TraceNumber)

        if plotFlag == True:
            plt.plot(x, y)
            plt.show()

        return x, y

    def avgMode(self, NbAverage):
        if int(NbAverage) > 1:
            self.activateAverageMode()
            print('Average mode on')
        for i in range(0, NbAverage):
            self.runSweepMode("single")
            print('Sweep ' + str(i) + ' is done')
        if int(NbAverage) > 1:
            self.deactivateAverageMode()
            print('Average mode off')

    def measure(self, TraceNumber=1, NbAverage=1, centerFreq=193500, span=100, Npoint = None, plotFlag = False):

        if  (Npoint != None):
            self.deactivateAutoNPoints()
            self.setNPoints(Npoint)

        #self.deleteAll()
        self.deactivateAverageMode()

        self.setScaleXUnit('GHz')
        self.setScaleYUnit('dB')

        self.setXResolution(0.1)
        self.setCenterFreq(centerFreq)
        self.setSpanFreq(span)

        self.runSweepMode('single')

        if int(NbAverage) > 1:
            print('Multiple sweep to get the average signal spectrum.')
            self.activateAverageMode()
            print('Average mode on')
            for i in range(0, NbAverage):
                self.runSweepMode("single")
                print('Sweep ' + str(i) + ' is done')
        if int(NbAverage) > 1:
            self.deactivateAverageMode()
            print('Average mode off')

        x, y = self.getData('GHz', 'dB', TraceNumber)
        self.setNpointAutoManual('auto')

        if plotFlag:
            plt.plot(x, y)
            plt.show()

        return x, y

    def s21Measure(self, TraceNumber=1, NbAverage=10, centerFreq=193500, sigBW=34, Npoint = None, plotFlag = False):
        spanF = math.ceil(sigBW * 3)
        self.deactivateAverageMode()

        if  (Npoint != None):
            self.setNpointAutoManual('manual')
            self.setNPoints(Npoint)

        #self.deleteAll()

        self.setScaleXUnit('GHz')
        self.setScaleYUnit('dB')

        self.setXResolution(0.1)
        self.setCenterFreq(centerFreq)
        self.setSpanFreq(spanF)

        self.avgMode(NbAverage=NbAverage)

        x_all, y_all = self.getData('GHz', 'dB', TraceNumber)

        plt.plot(x_all, y_all)
        plt.show()

        # find the central frequency
        idx = np.argmax(y_all, axis=0)
        fc = x_all[idx]
        print(fc)

        # only the positive freq is of interest + remove the fc
        freq = x_all[idx:] - fc
        spec = y_all[idx:]
        plt.plot( spec)
        plt.show()

        # find the nyquist freq
        tmp = np.where(freq >= sigBW)
        f_NY_idx = tmp[0][0]
        # The peak should be cut off and later interpolated in the filter design
        # 20 samples are enough
        freqTillNy = freq[20:f_NY_idx]
        specTillNy = spec[20:f_NY_idx]

        # spec = savgol_filter(spec, 5, 4)
        # plt.plot(freq, spec)
        # plt.show()

        # Do downsampling
        # freqTillNy = freqTillNy[0::10]
        # spectra = specTillNy[0::10]
        spectra = specTillNy

        # make sure freq and spec are even vectors
        if len(freqTillNy) % 2 == 1:
            freqTillNy = freqTillNy[0:len(freqTillNy)-1]
            spectra = spectra[0:len(freqTillNy)]

        # Normalization to 1 GHz
        smaller1 = np.where(freqTillNy < 1)
        f1 = smaller1[0][len(smaller1[0])-1]
        spectra = spectra-spectra[f1]

        plt.plot( spectra)
        plt.show()

        self.setNpointAutoManual('auto')

        return freqTillNy, spectra


if __name__ == "__main__":
    osa_inst = OsaApex()
    # print(osa_inst.getStopWavelength())
    # print(osa_inst.getStartWavelength())
    # print(osa_inst.ask('SPLINEVL?'))
    # # print(osa_inst.getXResolution())
    # print(osa_inst.ask('SPREFY?'))
    x, y = osa_inst.measure(TraceNumber=1, NbAverage=1, centerFreq=193400, span = 100, plotFlag=True)
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