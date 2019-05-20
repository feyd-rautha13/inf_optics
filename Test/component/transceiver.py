# /usr/bin/env python
# -*- coding : utf-8 -*-

'''
Reversion history

Rev 1.0 Thu May-09-2019
Created.


File description: 
Transsiver for groove
'''
__author__ = 'Sizhan Liu'
__version__ = "1.0"

import time
import re

class QSFPDD():
    def __init__(self, interface, card = 1, port = 8):
        '''
        initial QSFP-DD;
        dev as a groove Hal instance.
        '''
        self.card = card
        self.port = port
        self.dev = interface

    def reg_get(self, page = 0x00, offset = 0x00):
        '''
        Get specified register content, return a number in DEC base
        '''
        address = format(page**256+offset, '#06x')
        
        cmd = "hw {0} qsfp {1} rr {2} 1".format(self.card, self.port, address)
        self.dev.write(cmd)
        time.sleep(1)
        
        data = self.dev.read_raw().decode()
        data = re.split(r'\r|\n', data)
        data = [x for x in data if x != '']
        data = data[1].replace("[{0}]: ".format(address), "")
        data = int('0x'+data, 16)
        
        return data

    def reg_get2(self, page = 0x00, offset = 0x00):
        '''
        Get specified register content, return a number in DEC base
        '''
        address = format(page**256+offset, '#06x')
        
        cmd = "hw {0} qsfp {1} rr {2} 1".format(self.card, self.port, address)
        self.dev.write(cmd)
        time.sleep(1)
        
        data = self.dev.read_raw().decode()[-9:-7]

        data = int('0x'+data, 16)
        
        return data





