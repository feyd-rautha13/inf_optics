#####################################################################################
# Python API for IDP OSA
# Templete:     Robert Palmer
# Author:	Kunjen Zhang
# Date:		2017-08-04
#####################################################################################

import sys
import telnetlib
from decimal import Decimal

import numpy as np


class trace(object):
    def __init__(self, freq, p_tot, p_x, p_y):
        self.freq = freq
        self.p_tot = p_tot  # power will be in mW, not dBm
        self.p_x = p_x
        self.p_y = p_y


class idpOSA:
    def __init__(self, IP_address, port='3dBm'):
        ''' initializes ID OSA
            parameters:
                IP_address: IP address as string
        '''
        self.ip = IP_address
        self.port = port
        self.TCP_port = 2000
        self.scanRBW = 0.024  # Physical scan RBW in nm
        self.RBW = 0.5  # RBW in nm, not for the scan, only for calculations of OSNR, etc.
        self.OSAtype = 'ID OSA'
        self.tn = telnetlib.Telnet(self.ip, self.TCP_port)
        self.terminator = ';'
        self.timeout = 5
        self.trace = trace([], [], [], [])
        self.write('unit:x 1')
        self.write('step:freq 3.125000E+8')
        if port == '23dBm':
            self.write('input 1')
        elif port == '3dBm':
            self.write('input 2')
        else:
            print("Error!! port name is invalid.")
            sys.exit(1)

    def ask(self, commandstr):
        dummy = self.tn.read_until("", timeout=self.timeout)
        self.tn.write(commandstr + ";")
        answer = self.tn.read_until(self.terminator, timeout=self.timeout)
        return answer

    def write(self, commandstr):
        dummy = self.tn.read_until("", timeout=self.timeout)
        self.tn.write(commandstr + ";")
        # dummy = self.tn.read_until(self.terminator, timeout = self.timeout)
        dummy = self.tn.read_until(self.terminator, timeout=self.timeout)
        if "ERR" in dummy: print "Communication error with ID OSA."
        self.tn.write("*wai;")
        dummy = self.tn.read_until(self.terminator, timeout=self.timeout)
        return

    def sweep(self, num_averages=3, num_points=0):
        ''' Sweeps the OSA num_averages-times and stores results in self.trace.'''
        y_lin_total = 0
        for ii in range(num_averages):
            self.write("SGL")
            x = self.ask("xauto?")
            y = self.ask("y?")
            self.trace.freq = np.array(map(float, x[:-1].split(','))) * 1e-12  # in THz
            y = np.array(map(float, y[:-1].split(',')))
            y_lin = np.array([10 ** (0.1 * yy) for yy in y])  # in mW
            y_lin_total = y_lin_total + y_lin
        self.trace.p_tot = y_lin_total * 1. / num_averages
        self.trace.p_tot = self.trace.p_tot[::-1]
        self.trace.freq = self.trace.freq[::-1]

    def setStartStopFreq(self, start, stop):
        ''' Sets start and stop frequency of the OSA in THz. '''
        # Minimum start freq for ID OSA is 191.25THz
        if start < 191.25:
            start = 191.25

        start = "{:.5E}".format(Decimal(str(start * 1e12)))
        stop = "{:.5E}".format(Decimal(str(stop * 1e12)))
        self.write(str("star " + start))
        self.write(str("stop " + stop))

    def setCenterSpanFreq(self, center, span):
        ''' Sets Center frequency and span of the OSA in THz. '''
        start = center - span * 1. / 2
        stop = center + span * 1. / 2
        self.setStartStopFreq(start, stop)

    def setStartStopWL(self, startWLnm, stopWLnm):
        ''' Sets start and stop wavelength of the OSA in nm. '''
        c = 299792458.0  # speed of light
        start = c / stopWLnm / 1000
        stop = c / startWLnm / 1000
        center = (start + stop) * 1. / 2
        span = stop - start
        self.setCenterSpanFreq(center, span)

    def setCenterSpanWL(self, centerWLnm, spanWLnm):
        ''' Sets center wavelength and span of the OSA in nm. '''
        c = 299792458.0  # speed of light
        stopWLnm = centerWLnm + spanWLnm * 1. / 2
        startWLnm = centerWLnm - spanWLnm * 1. / 2
        start = c / stopWLnm / 1000
        stop = c / startWLnm / 1000
        center = (start + stop) * 1. / 2
        span = stop - start
        self.setCenterSpanFreq(center, span)

    def getSpectrum(self):
        ''' Returns the spectrum from last frequency sweep in dBm (triggered by the internal sweep function). '''
        power = []
        for ii in self.trace.p_tot:
            power.append(10 * np.log10(abs(ii)))  # Conversion to dBm
        return self.trace.freq, power

    def findMax(self):
        ''' Finds the maximum power in the spectrum and returns max. power, corresponding frequency and index. '''
        pow = list(self.trace.p_tot)
        freq = list(self.trace.freq)
        MaxPow = max(pow)
        indexMP = pow.index(MaxPow)
        f_max = freq[indexMP]
        return MaxPow, f_max, indexMP

    def getOSNR(self, ctFreq=194.1, sBw=0.0625, nDistance=0.04, avg=3):
        nBw = 0.025  # 25GHz = 0.2nm

        C1 = ctFreq - sBw / 2
        C2 = ctFreq + sBw / 2
        NL2 = ctFreq - nDistance
        NL1 = NL2 - nBw
        NR1 = ctFreq + nDistance
        NR2 = NR1 + nBw
        osnr = self.get6pointOSNR(C1, C2, NL1, NL2, NR1, NR2, avg)
        print('Curr OSNR: %.2f dB' % osnr)
        return osnr

    def get6pointOSNR(self, C1, C2, NL1, NL2, NR1, NR2, avg):
        centerFreq = C1 + (C2 - C1) / 2.
        self.setStartStopFreq(centerFreq - 0.1, centerFreq + 0.1)
        self.write('STEP 0.3125e+9')  # scan RBW = 315MHz
        self.sweep(avg)

        CP = self.mwIntegrate(self.trace.freq, self.trace.p_tot, C1, C2)
        NLP = self.mwIntegrate(self.trace.freq, self.trace.p_tot, NL1, NL2)
        NRP = self.mwIntegrate(self.trace.freq, self.trace.p_tot, NR1, NR2)

        # Noise Power Density
        NPD = (NLP / (NL2 - NL1) + NRP / (NR2 - NR1)) / 2

        # total power of background noise in channel
        CN = NPD * (C2 - C1)

        # Power in channel from signal *only*
        S = CP - CN
        sdBm = self.mW2dBm(S)
        print "Signal Power = {0}dB".format(str(sdBm))

        # Noise referenced to reference BW 0.1nm
        refBw = 0.0125
        N = NPD * refBw
        ndBm = self.mW2dBm(N)
        print "Noise (0.1nm) Power = {0}dB".format(str(ndBm))

        return self.mW2dBm(S / N)

    def getSigPow(self, noisePointSep_nm=0.6, RBW_nm=0):
        ''' Finds maximum in spectrum and calculates OSNR. '''
        if RBW_nm == 0:
            RBW_nm = self.RBW
        MaxPow, f_max, indexMP = self.findMax()
        c = 299792458.0  # speed of light
        df = (f_max ** 2) * 1.0 / c * (RBW_nm) * 10 ** 3
        noise_sep_THz = (f_max ** 2) * 1.0 / c * (noisePointSep_nm) * 10 ** 3
        print 'df = ', str(df)
        C1 = round(f_max - df * 1. / 2, 3)  # Channel start frequency
        C2 = round(f_max + df * 1. / 2, 3)  # Channel stop frequency
        NL1 = round(f_max - noise_sep_THz - df * 1. / 2, 3)  # Noise Left-side start frequency
        NL2 = round(f_max - noise_sep_THz + df * 1. / 2, 3)  # Noise Left-side stop frequency
        NR1 = round(f_max + noise_sep_THz - df * 1. / 2, 3)  # Noise Right-side start frequency
        NR2 = round(f_max + noise_sep_THz + df * 1. / 2, 3)  # Noise Right-side stop frequency

        CP = self.mwIntegrate(self.trace.freq, self.trace.p_tot, C1, C2)
        NLP = self.mwIntegrate(self.trace.freq, self.trace.p_tot, NL1, NL2)
        NRP = self.mwIntegrate(self.trace.freq, self.trace.p_tot, NR1, NR2)

        # Noise Power Density
        NPD = (NLP / (NL2 - NL1) + NRP / (NR2 - NR1)) / 2

        # total power of background noise in channel
        CN = NPD * (C2 - C1)

        # Power in channel from signal *only*
        S = CP - CN
        S_dBm = (10 * np.log10(S))

        return S_dBm

    def getChannelPower(self, ch_freq, num_averages=3, noisePointSep_nm=0.6, RBW_nm=0):
        self.sweep(num_averages)
        freq, pow = self.getSpectrum()
        c = 299792458.0  # speed of light
        df = 0.05  # 50GHz window
        noise_sep_THz = 0.05  # 50GHz
        C1 = round(ch_freq - df * 1. / 2, 3)  # Channel start frequency
        C2 = round(ch_freq + df * 1. / 2, 3)  # Channel stop frequency

        CP = self.mwIntegrate(self.trace.freq, self.trace.p_tot, C1, C2)

        S = CP  # - CN
        S_dBm = (10 * np.log10(S + 1e-10))

        return S_dBm

    # Power must be in units of mW
    def mwIntegrate(self, freq, power, fstart, fstop):
        dF = abs(freq[-1] - freq[0]) / freq.size
        i = np.searchsorted(freq, [fstart, fstop])
        return dF * np.sum(power[i[0]:i[1]]) / 0.00015

    # Power mW to dBm
    def mW2dBm(self, mW):
        dBm = round(10 * np.log10(mW), 2)
        return dBm

    def extractS21(self, centerFreq, num_averages=10, UseMaxAsCenter=False):
        self.setCenterSpanFreq(centerFreq, 0.15)
        self.sweep(num_averages)
        freq, pow = self.getSpectrum()
        import matplotlib.pyplot as plt
        plt.figure(22)
        plt.plot(freq, pow)
        # Use maximum of spectrum as new center frequency - can result in an offset, if carrier is completely suppressed
        if UseMaxAsCenter:
            MaxPow, f_max, indexMP = self.findMax()
            print 'frequency offset = ', centerFreq - f_max
            centerFreq = f_max
        df = freq[1] - freq[0]
        freq_norm = freq - centerFreq
        # Find closest point to centerFreq
        freq_norm_square = freq_norm ** 2
        indexCenterFreq = list(freq_norm_square).index(min(list(freq_norm_square)))
        index30GHz = indexCenterFreq + int(0.03 / df) + 1
        indexNeg30GHz = indexCenterFreq - int(0.03 / df) - 1
        index_offset = 2
        S21_freq = freq_norm[indexCenterFreq + index_offset:index30GHz + 1]
        S21_pow_right = pow[indexCenterFreq + index_offset:index30GHz + 1]
        S21_pow_left = pow[indexNeg30GHz:indexCenterFreq - index_offset + 1]
        S21_pow_left = S21_pow_left[::-1]
        S21_pow = (np.array(S21_pow_right) + np.array(S21_pow_left)) * 1. / 2
        index1GHz = int(0.001 / df) - index_offset + 1
        S21_pow = S21_pow - S21_pow[index1GHz]
        S21_pow_right = S21_pow_right - S21_pow_right[index1GHz]
        S21_pow_left = S21_pow_left - S21_pow_left[index1GHz]
        return S21_freq, S21_pow, S21_pow_right, S21_pow_left

    def measure(self, TraceNumber=1, NbAverage=1, centerFreq=193400, span=100, plotFlag=True):
        self.setCenterSpanFreq(centerFreq, 0.15)
        self.sweep(NbAverage)
        freq, pow = self.getSpectrum()

        if plotFlag:
            import matplotlib.pyplot as plt
            plt.figure(22)
            plt.plot(freq, pow)

        return freq, pow


if __name__ == '__main__':
    osa = idpOSA("172.29.153.182", '3dBm')

    ctFreq = 194.1  # THz
    sBw = 0.0625  # THz
    nDistance = 0.04  # THz

    while True:
        osnr = osa.getOSNR(ctFreq, sBw, nDistance, 3)
        print "------------------------------------------OSNR = {0}dB".format(str(osnr))
