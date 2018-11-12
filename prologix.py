# /usr/bin/env python
# -*- coding : utf-8 -*-

__author__ = 'Sizhan Liu'
__version__ = "1.0"

'''
Creat Porlogix Ethernet interface

reference:
1. Yingkan Chen's VOA driver
2. https://bitbucket.org/martijnj/telepythic Copyright 2014 by Martijn Jasperse

'''

import time
from TCPinterface import TCP


############### --Connectiong -- ###############
class Prologix(TCP):
    def __init__(self, host, port):
        '''Setup a remote connection for prologix'''
        
        self._host = host
        self._port = port
        TCP.__init__(self, self._host, self._port)
        time.sleep(1)

        # set prologix as controller mode
        self.write("++mode 1")
        # Turn off read-after-write function
        self.write("++auto 0")    
        # set read timeout time is 3000ms(max) 
        self.write("++read_tmo_ms 3000")      
        # Do not append CR or LF to GPIB data
        self.write("++eos 3")
        # Assert EOI with last byte to indicate end of data
        self.write("++eoi 1")

########## --data parse for luna only -- ###############   
    def setAddr(self, GPIBaddress):
        '''
        Setting instruments GPIB address
        '''
        address = str(GPIBaddress)
        address = "++addr " + address
        self.write(address)

    def close(self):
        '''Close remote connection for Prologix GPIB card'''       
        self.TCP_close()


########## --super class alternative method --- #######
    def write(self,cmd):
        '''
        Prologix card needs "\n" as end.
        '''     
        cmd = str(cmd) + '\n'
        TCP.write(self,cmd)
        
    def read(self, flag = None , endnumber = None):
        '''
        If decvice response time larger than TCP time out. 
        '''
        self._flag = flag
        self._endno = endnumber
        
        if self._flag == None:
            data = TCP.read_raw(self)
        else:
            data = TCP.read_raw(self)
            while True:
                try:
                    if len(data) <= 1 or data[-1*endnumber:] != self._flag:
                        data += TCP.read_raw(self)
                    else:
                        break   
                except:
                    pass
        return data
    
    def query(self, cmd, flag = None, endnumber = None):
        '''query GPIB command result from prologix'''
        self._flag = flag
        self._endnumber = endnumber
        
        self.write(cmd)
        self.write("++read eoi")

        if self._flag == None: 
            data = self.read()
        else:
            data = self.read(flag = self._flag, endnumber = self._endnumber)
        return data

