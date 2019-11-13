# -------------------------------------------------------------------------------
# Name:        os_fitel.py
# Purpose:     
#              
#
# Author:      Yingkan Chen
#
# Version:     
#
# Created:     27/01/2017
# Copyright:   (c) Coriant R&D GmbH 2016
# -------------------------------------------------------------------------------

# System level import
import time
# site-package import

# 3rd party project module import

# Project module import
from module.Prologix import Prologix


class os_pro800(Prologix):
    def __init__(self, host="10.50.22.98", port=1234, addr="10", sock=None):
        Prologix.__init__(self, host, port, addr, sock)
        # print('%s initializing ... ' % self.getID().replace('\n', ''))

    def getID(self):
        return self.ask("*IDN?\n")

    def select_slot(self, slot):
        self.write(':SLOT %d' % slot)

    def switch2Port(self, portNo, slot=1):
        self.select_slot(slot)
        self.write(':OSW %d' % portNo)
        print('Target   to Slot %d Port %d' % (slot, portNo))
        time.sleep(1)
        print('Switched to Slot %s Port %s' % (self.get_curr_slot(), self.currClosedPort()))

    def currClosedPort(self):
        return self.ask(':OSW?').replace('\n', '').split(' ')[-1]

    def get_curr_slot(self):
        return self.ask(':SLOT?').replace('\n', '').split(' ')[-1]


if __name__ == "__main__":
    os_inst = os_pro800()
    # os_inst.switch2Port(slot=2, portNo=5)
    # os_inst.switch2Port(slot=1, portNo=5)
    os_inst.switch2Port(slot=1, portNo=2)
    os_inst.switch2Port(slot=2, portNo=2)
    #os_inst.switch2Port(slot=2, portNo=6)
    #os_inst.switch2Port(slot=1, portNo=1)
