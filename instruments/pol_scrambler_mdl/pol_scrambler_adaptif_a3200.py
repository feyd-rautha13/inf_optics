# -------------------------------------------------------------------------------
# Name:        pol_scrambler_adaptif_a3200.py
# Purpose:     
#              
#
# Author:      Yingkan Chen
#
# Version:     
#
# Created:     08/11/2017
# Copyright:   (c) Coriant R&D GmbH 2016
# -------------------------------------------------------------------------------

# System level import

# site-package import

# 3rd party project module import

# Project module import
from module.Prologix import Prologix


class pol_scrambler_adaptif_a3200(Prologix):
    def __init__(self, host="10.50.22.99", port=1234, addr="30", sock=None):
        Prologix.__init__(self, host, port, addr, sock)
        print('%s initializing ... ' % self.getID().replace('\n', ''))

    def getID(self):
        return self.ask("*IDN?\r\n")


if __name__ == "__main__":
    ps_inst = pol_scrambler_adaptif_a3200()
