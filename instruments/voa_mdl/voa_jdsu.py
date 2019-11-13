#-------------------------------------------------------------------------------
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
#-------------------------------------------------------------------------------

# System level import
import traceback

from module.Prologix import Prologix


class voa_jdsu(Prologix):
    def __init__(self, host = "10.148.255.133", port = 1234, addr = "4", sock = None):
        Prologix.__init__(self, host, port, addr, sock)
        if self.voaIsRunning:
            print('VOA JDSU is running.')
        self.setShutterOn()


    def read_att_value(self):
        str = 'NA'
        self.setAddr()
        while True:
            try:
               str = self.ask('ATT?')
               print(self.__class__.__name__ + ' has value %s' % str)
            except:
                print(traceback.format_exc())
                continue
            break

        return float(str)

    def set_att_value(self, val):
        self.setAddr()
        self.write('ATT %.2f' % val)
        print(self.__class__.__name__ + ' is setting value to %.2f' % val)

    def closeConnection(self):
        print(self.__class__.__name__ + ' is closed.')
        self.sock.close()

    def setShutterOn(self):
        self.setAddr()
        self.write('D 0')
        print(self.__class__.__name__ + 'Shutter on')

    def setShutterOff(self):
        self.setAddr()
        self.write('D 1')
        print(self.__class__.__name__ + 'Shutter off')

if __name__ == "__main__":
    voa_inst_ = voa_jdsu(host='10.50.22.99', port=1234, addr='17')
    print(voa_inst_.ask('IDN?'))

    print(voa_inst_.read_att_value())

    # voa_inst_.set_att_value(40.62)
    voa_inst_.setShutterOff()

    print(voa_inst_.read_att_value())