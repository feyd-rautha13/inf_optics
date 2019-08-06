#####################################################################################
# Finisar_WaveAnalyzer_API
# Status: 2016-07-19: First version. Robert Palmer, Coriant R&D
#####################################################################################

import time
import telnetlib
# import requests
import math
import numpy as np
from collections import namedtuple
from decimal import Decimal


class myData(object):
    def __init__(self, freq, p_tot, p_x, p_y):
        self.freq = freq
        self.p_tot = p_tot  # power will be in mW, not dBm
        self.p_x = p_x
        self.p_y = p_y


class ID_OSA_CTRL_fn:
    def __init__(self, IP_address, port='HighSens', fakeOSA=False):
        ''' initializes Finisar WaveAnalyzer
            parameters:
                IP_address: IP address as string 
        '''
        self.ip = IP_address
        self.port = port
        self.TCP_port = 2000
        self.scanRBW = 0.024  # Physical scan RBW in nm
        self.RBW = 0.5  # RBW in nm, not for the scan, only for calculations of OSNR, etc.
        self.OSAtype = 'ID OSA'
        self.fakeOSA = fakeOSA
        self.tn = telnetlib.Telnet(self.ip, self.TCP_port)
        self.terminator = ';'
        self.timeout = 5
        self.data = myData([], [], [], [])
        self.write('unit:x 1')
        self.write('step:freq 3.125000E+8')

    def read_until_finished_or_error(self):
        t0 = time.time()
        t1 = time.time()
        total_time = t1 - t0
        done = False
        while total_time < self.timeout or done:
            time.sleep(1)
            r = self.tn.read_some()
            if any(x in r for x in ["self.terminator", "ERR"]):
                done = True
                if "ERR" in r:
                    print "Communication error with ID OSA."
            t1 = time.time()
            total_time = t1 - t0
        return r

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
        ''' Sweeps the OSA num_averages-times and stores results in self.data '''
        y_lin_total = 0
        for ii in range(num_averages):
            self.write("SGL")
            x = self.ask("xauto?")
            y = self.ask("y?")
            self.data.freq = np.array(map(float, x[:-1].split(','))) * 1e-12  # in THz
            y = np.array(map(float, y[:-1].split(',')))
            y_lin = np.array([10 ** (0.1 * yy) for yy in y])  # in mW
            y_lin_total = y_lin_total + y_lin
        self.data.p_tot = y_lin_total * 1. / num_averages
        self.data.p_tot = self.data.p_tot[::-1]
        self.data.freq = self.data.freq[::-1]

    def setStartStopFreq(self, start, stop):
        ''' Sets start and stop frequency of the OSA in THz. '''
        # center = (start+stop)*1./2
        # span=stop-start
        # self.setCenterSpanFreq(center, span)

        # Minimum start freq for ID OSA is 191.25THz
        if start < 191.25:
            start = 191.25
        # Minimum start freq for ID OSA is 191.25THz
        if stop > 196.125:
            stop = 196.125
        start = "{:.5E}".format(Decimal(str(start * 1e12)))
        stop = "{:.5E}".format(Decimal(str(stop * 1e12)))
        # print "start:\t", start
        # print "stop:\t", stop
        self.write(str("star " + start))
        self.write(str("stop " + stop))
        self.write(str(
            "star " + start))  # write second time in case first commend was ignored due to conflict with upper frequency limit.
        # print self.ask("span?")
        # print self.ask("cent?")

    def setCenterSpanFreq(self, center, span):
        ''' Sets Center frequency and span of the OSA in THz. '''
        start = center - span * 1. / 2
        stop = center + span * 1. / 2
        self.setStartStopFreq(round(start, 2), round(stop, 2))

        # center = "{:.5E}".format(Decimal(str(center * 1e12)))
        # span = "{:.5E}".format(Decimal(str(span * 1e12)))
        # self.write(str("span "+span))
        # self.write(str("cent "+center))

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
        start = c / stopWLnm / 1000.
        stop = c / startWLnm / 1000.
        center = (start + stop) * 1. / 2
        span = stop - start
        self.setCenterSpanFreq(center, span)

    def setOsnrMeasurement(self, centerWLnm=1551.19, spanWLnm=8, RBW_dummy=0.5):
        # self.setSweepMode('Single')
        self.setCenterSpanWL(centerWLnm, spanWLnm)
        self.RBW = RBW_dummy

    def getSpectrum(self):
        ''' Returns the spectrum from last frequency sweep in dBm (triggered by the internal sweep function). '''
        power = []
        for ii in self.data.p_tot:
            power.append(10 * np.log10(abs(ii)))  # Conversion to dBm
        return self.data.freq, power

    def findMax(self):
        ''' Finds the maximum power in the spectrum and returns max. power, corresponding frequency and index. '''
        pow = list(self.data.p_tot)
        freq = list(self.data.freq)
        MaxPow = max(pow)
        indexMP = pow.index(MaxPow)
        f_max = freq[indexMP]
        return MaxPow, f_max, indexMP

    def getOSNR(self, noisePointSep_nm=0.5, RBW_nm=0):  # TBD
        ''' Finds maximum in spectrum and calculates OSNR. '''
        self.sweep()
        if RBW_nm == 0:
            RBW_nm = self.RBW
        MaxPow, f_max, indexMP = self.findMax()
        c = 299792458.0  # speed of light
        df = (f_max ** 2) * 1.0 / c * (RBW_nm) * 10 ** 3
        noise_sep_THz = (f_max ** 2) * 1.0 / c * (noisePointSep_nm) * 10 ** 3
        # print 'f_max = ', str(f_max)
        # print 'df = ', str(df)
        # print 'noise_sep_THz = ', noise_sep_THz
        C1 = round(f_max - df * 1. / 2, 3)  # Channel start frequency
        C2 = round(f_max + df * 1. / 2, 3)  # Channel stop frequency
        NL1 = round(f_max - noise_sep_THz - df * 1. / 2, 3)  # Noise Left-side start frequency
        NL2 = round(f_max - noise_sep_THz + df * 1. / 2, 3)  # Noise Left-side stop frequency
        NR1 = round(f_max + noise_sep_THz - df * 1. / 2, 3)  # Noise Right-side start frequency
        NR2 = round(f_max + noise_sep_THz + df * 1. / 2, 3)  # Noise Right-side stop frequency

        CP = self.wa_integrate(self.data.freq, self.data.p_tot, C1, C2)
        NLP = self.wa_integrate(self.data.freq, self.data.p_tot, NL1, NL2)
        NRP = self.wa_integrate(self.data.freq, self.data.p_tot, NR1, NR2)
        # Noise Power Density
        NPD = (NLP / (NL2 - NL1) + NRP / (NR2 - NR1)) / 2

        # total power of background noise in channel
        CN = NPD * (C2 - C1)

        # Power in channel from signal *only*
        S = CP - CN
        # print 'Signal power: ',str(10*np.log10(S))
        # Noise referenced to RefBW
        RefBW = 0.0125
        N = NPD * RefBW
        OSNR = round(10 * np.log10(S / N + 0.00001), 2)
        # print 'OSNR = ', OSNR
        # print 'S, N :', S, N
        return OSNR

    def get6pointOSNR(self, C1, C2, NL1, NL2, NR1, NR2, averages=10, timeout=1, RefBW=0.0125):
        d = self.takeScan(averages, timeout, 'mW')
        CP = self.wa_integrate(d.freq, d.p_tot, C1, C2)
        NLP = self.wa_integrate(d.freq, d.p_tot, NL1, NL2)
        NRP = self.wa_integrate(d.freq, d.p_tot, NR1, NR2)

        # Noise Power Density
        NPD = (NLP / (NL2 - NL1) + NRP / (NR2 - NR1)) / 2

        # total power of background noise in channel
        CN = NPD * (C2 - C1)

        # Power in channel from signal *only*
        S = CP - CN
        # print 'Signal power: ',str(10*np.log10(S))
        # Noise referenced to RefBW
        N = NPD * RefBW
        return round(10 * np.log10(S / N), 2)

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

        CP = self.wa_integrate(self.data.freq, self.data.p_tot, C1, C2)
        NLP = self.wa_integrate(self.data.freq, self.data.p_tot, NL1, NL2)
        NRP = self.wa_integrate(self.data.freq, self.data.p_tot, NR1, NR2)

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

        # NL1 = round(freq-noise_sep_THz -df*1./2,3)      #Noise Left-side start frequency
        # NL2 = round(freq-noise_sep_THz +df*1./2,3)     #Noise Left-side stop frequency
        # NR1 = round(freq+noise_sep_THz -df*1./2,3)      #Noise Right-side start frequency
        # NR2 = round(freq+noise_sep_THz +df*1./2,3)     #Noise Right-side stop frequency

        CP = self.wa_integrate(self.data.freq, self.data.p_tot, C1, C2)
        # NLP = self.wa_integrate(self.data.freq, self.data.p_tot, NL1, NL2)
        # NRP = self.wa_integrate(self.data.freq, self.data.p_tot, NR1, NR2)

        # Noise Power Density
        # NPD = (NLP/(NL2-NL1) + NRP/(NR2-NR1))/2

        # total power of background noise in channel
        # CN = NPD * (C2 - C1)

        # Power in channel from signal *only*
        S = CP  # - CN
        S_dBm = (10 * np.log10(S + 1e-10))

        return S_dBm

    def extractS21(self, centerFreq, num_averages=10, UseMaxAsCenter=False):
        self.setCenterSpanFreq(centerFreq, 0.15)
        self.sweep(num_averages)
        freq, pow = self.getSpectrum()
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

    def takeScan(self, averages=1, timeout=1, units='dBm'):
        freq, p_tot1, p_x1, p_y1, _ = self.wa_get_data_linear(timeout)
        if averages > 1:
            for i in range(1, averages):
                _, p_tot2, p_x2, p_y2, _ = self.wa_get_data_linear(timeout)
                p_tot1 += p_tot2
                p_x1 += p_x2
                p_y1 += p_y2

        p_tot1 /= averages
        p_x1 /= averages
        p_y1 /= averages

        if units != 'mW':
            p_tot1 = 10 * np.log10(abs(p_tot1))
            p_x1 = 10 * np.log10(abs(p_x1))
            p_y1 = 10 * np.log10(abs(p_y1))

        WAData = namedtuple('WAData', ['freq', 'p_tot', 'p_x', 'p_y'])
        return WAData(freq, p_tot1, p_x1, p_y1)

        # Power must be in units of mW

    def wa_integrate(self, freq, power, fstart, fstop):
        dF = abs(freq[-1] - freq[0]) / freq.size
        i = np.searchsorted(freq, [fstart, fstop])
        # print "freqs: "+str(fstart)+", "+str(fstop)+", "+str(freq)
        # print "indices: "+str(i)
        return dF * np.sum(power[i[0]:i[1]]) / 0.00015


        # def wa_get_data(self,timeout=1):
        #     self.wa_wait_for_unique_scan(timeout)
        #     m = requests.get('http://'+self.ip+'/wanl/data/bin').content
        #     data = np.fromstring(m[1000:], dtype=int)
        #     freq = data[0::5]/1000000.0
        #     p_tot = data[1::5]/1000.0
        #     p_x = data[2::5]/1000.0
        #     p_y = data[3::5]/1000.0
        #     trigger = data[4::5]
        #     return freq, p_tot, p_x, p_y, trigger
        #
        # def wa_get_data_linear(self, timeout=1):
        #     self.wa_wait_for_unique_scan(timeout)
        #     m = requests.get('http://'+self.ip+'/wanl/lineardata/bin').content
        #
        #     data1 = np.fromstring(m[1000:], dtype='int')
        #     data2 = np.fromstring(m[1000:], dtype='float32')
        #
        #     freq = data1[0::5]/1000000.0
        #     p_tot = data2[1::5]
        #     p_x = data2[2::5]
        #     p_y = data2[3::5]
        #     trigger = data1[4::5]
        #     return freq, p_tot, p_x, p_y, trigger
        #
        # def wa_wait_for_unique_scan(self,timeout=1):
        #     start_time = time.time()
        #     scanid = self.wa_get_scan_id()
        #     while time.time()-start_time < timeout and self.wa_get_scan_id()==scanid:
        #         time.sleep(0.01)
        #
        # def wa_get_scan_id(self):
        #     m = requests.get('http://'+self.ip+'/wanl/scan/status')
        #     scanid = m.json()['scanid']
        #     return scanid


if __name__ == "__main__":
    osa_inst = ID_OSA_CTRL_fn('172.29.153.182')

    # while True:
    #     print(osa_inst.getOSNR())
    # S21_freq, S21_pow, S21_pow_right, S21_pow_left = osa_inst.extractS21(centerFreq=194.1)
    import matplotlib.pyplot as plt

    plt.figure(22)
    plt.plot(S21_freq, S21_pow)
    plt.show()
