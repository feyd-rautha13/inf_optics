# -------------------------------------------------------------------------------
# Name:        OsaAgilent.py
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
import time
import math

# site-package import
import telnetlib

# 3rd party project module import
from random import uniform
from PyQt4.QtCore import QThread
from numpy import linspace
from abc import ABCMeta
from PyQt4.QtCore import QObject


class OsaAgilent:
    def __init__(self, ipaddr='10.50.22.48', ipport=10001):

        self.host_ = ipaddr
        self.port_ = ipport
        self.user_ = '\"anonymous\"'  # self.xmlParser_.ReadAttr(self.chosenConfig_, 'osa', 'user')

        self.ter_ = '\r\n'  # Terminator
        self.test_ = False
        self.aq_6319_ = False
        self.map_sweep_mode_ = {3: 'AUTO', 2: 'REPEAT', 1: 'SINGLE'}

        print('OSA init')
        # === Connect ===
        if not self.test_:
            self.tn = telnetlib.Telnet(self.host_, self.port_)
            self.tn.write(self.ter_)
            if not self.aq_6319_:
                # logging in ...
                self.tn.write('open ' + self.user_ + self.ter_)
                qq = self.tn.read_until('CRAM-MD5.' + self.ter_)
                print(qq)
                self.tn.write(self.ter_)  # password not required
                print(self.tn.read_until('ready' + self.ter_))
                # OK, we are in

        self.isRunning = True

    def osaRun(self):
        print('OSA run')
        while self.isRunning:
            time.sleep(1)

        if not self.test_:
            self.tn.close()
        print('OSA stopped')

    def stop(self):
        self.isRunning = False

    # ==================================================
    # Sub routine
    # Send Remote Command
    # ==================================================
    def sendLan(self, strData):
        if self.test_:
            print('SendLan', strData)
        else:
            self.tn.write(strData + self.ter_)

    # ==================================================
    # Sub routine
    # Receive query data
    # ==================================================
    def receiveLan(self, command=''):
        self.sendLan(command)
        return self.tn.read_until(self.ter_)

    def changeWL(self, start, stop):
        self.sendLan(':sens:wav:star {:.3f}nm'.format(start))
        self.sendLan(':sens:wav:stop {:.3f}nm'.format(stop))
        self.sendLan(':disp:trac:x[:scal]:star {:.3f}nm'.format(start))
        self.sendLan(':disp:trac:x[:scal]:stop {:.3f}nm'.format(stop))

    def changeRefScale(self, ref, scale):
        self.sendLan(':disp:trac:y1:rlev {:.1f}dbm'.format(ref))
        self.sendLan(':disp:trac:y1:pdiv {:.1f}db'.format(scale))

    def getStartStop(self):
        if self.test_:
            start = 1520.
            stop = 1560.
        else:
            q = self.receiveLan(':sens:wav:star?')
            start = float(q) * 1e9
            q = self.receiveLan(':sens:wav:stop?')
            stop = float(q) * 1e9
        return start, stop

    def getRefScale(self):
        if self.test_:
            ref = 10.
            scale = 10.
            rpos = 8.
        else:
            q = self.receiveLan(':disp:trac:y1:rlev?')
            ref = float(q)
            q = self.receiveLan(':disp:trac:y1:pdiv?')
            scale = float(q)
            q = self.receiveLan(':disp:trac:y1:rpos?')
            rpos = float(q)
        return ref, scale, rpos

    def sweep(self):
        self.sendLan(':INITiate')

    def abort(self):
        self.sendLan(':ABORt')

    def reset(self):
        self.sendLan('*RST')

    def getData(self, trace):
        if self.test_:
            x = linspace(1520e-9, 1540e-9)
            freq = uniform(1e+9, 10e+9)
            amp = uniform(.5, 50)
            off = uniform(-20, 0)
            y = [amp * math.sin(2 * math.pi * freq * a) + off for a in x]
        else:
            x = self.receiveLan(':trac:x? ' + trace).split(',')
            y = self.receiveLan(':trac:y? ' + trace).split(',')
        return x, y

    def getOSNR(self):
        self.sendLan(':CALCulate:CATegory? OSNR|WDM|')
        self.sendLan('CALCulate[:IMMediate]')
        osnrValue = self.receiveLan(':CALCulate:DATA:CSNR?')
        print('Curr OSNR: %.2f dB' %  float(osnrValue))
        return float(osnrValue)

    def getSweepMode(self):
        SweepMode = int(self.receiveLan(':INITiate:SMODe?'))
        return self.map_sweep_mode_[SweepMode]

    def setSweepMode(self, SweepMode):
        self.sendLan(':INITiate:SMODe ' + SweepMode)

    def setCalibrationZERO(self, value):
        if value in ['on', 'off']:
            self.sendLan(':CALibration:ZERO ' + value)
        else:
            print('value must be either \'on\' or \'off\'')

    def close(self):
        self.tn.close()

    def disconnect(self):
        self.close()

    def closeConnection(self):
        self.disconnect()

if __name__ == '__main__':
    osa_inst = OsaAgilent(ipaddr='10.50.22.204')
    osa_inst.sweep()
    OSNR = osa_inst.getOSNR()
    print(OSNR)
    # SweepMode = osa_inst.getSweepMode()
    # print(SweepMode)
    #
    # for sm in osa_inst.map_sweep_mode_.values():
    #     print(sm)
    #     osa_inst.setSweepMode(sm)
    #     SweepMode = osa_inst.getSweepMode()
    #     print(SweepMode)
    #
    #     osa_inst.setCalibrationZERO('off')
    #
    osa_inst.tn.close()
    # osa_inst.changeWL(1558.58-2, 1558.58+2)
