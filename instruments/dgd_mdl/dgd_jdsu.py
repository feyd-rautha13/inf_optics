#-------------------------------------------------------------------------------
# Name:        dgd_JDSU.py
# Purpose:     
#              
#
# Author:      Yingkan Chen
#
# Version:     
#
# Created:     10/07/2017
# Copyright:   (c) Coriant R&D GmbH 2016
#-------------------------------------------------------------------------------

# System level import

# site-package import
from module.dgd_mdl.DGD import DGD
# 3rd party project module import
import traceback
# Project module import


class dgd_jdsu(DGD):
    def __init__(self, host= '10.50.22.99', port = 1234, addr='4', sock= None):
        DGD.__init__(self, host, port, addr, sock)

        if self.voaIsRunning:
            print('DGD JDSU is running.')

    def read_dgd_value(self):
        str = 'NA'
        self.setAddr()
        while True:
            try:
                str = self.ask('PMD?')
                print(self.__class__.__name__ + ' has value %s' % str)
            except:
                print(traceback.format_exc())
                continue
            break

        return str

    def set_dgd_value(self, val):
        while int(float(self.read_dgd_value().replace('\r\n', ''))) != val:
            self.setAddr()
            self.write('PMD %.2f' % val)
            print(self.__class__.__name__ + ' is setting value to %.2f' % val)
        self.read_dgd_value()

    def closeDGDConnection(self):
        print(self.__class__.__name__ + ' is closed.')
        self.sock.close()

if __name__ == "__main__":
    inst = dgd_jdsu()
    # inst.read_dgd_value()
    inst.set_dgd_value(50)
    # inst.read_dgd_value()
