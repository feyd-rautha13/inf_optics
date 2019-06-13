# /usr/bin/env python
# -*- coding : utf-8 -*-

__author__ = 'Sizhan Liu'
__version__ = "1.0"

'''
EXFO FTB-8 Chasis interface
'''

path1 =  'D:\\work\\coding\\python\\inf_optics\\interface\\'

import sys
sys.path.append(path1)

import time
import re
import pylab as pl
from TCPinterface import TCP


ip = '172.29.150.191'
port = 5025

############### --Connectiong -- ###############
class FTB8(TCP):
    def __init__(self, host, port):
        '''Setup a remote connection for FTB'''
        self._host = host
        self._port = port
        super().__init__(self._host, self._port)
        time.sleep(1)
       
        #command = "*CLS"
        #self.write(command)
        #time.sleep(1)

        #check if you expect result
        #A = self.deviceID.decode().replace("\x00","").lower()
        #if A=='optical vector analyzer':
        #    print("--> Welcome to passive test platform :) --")
        #else:
        #    print('Wrong connection!')
        #    self.close()

    def close(self):
        '''Close remote connection for FTB-8'''
        self.write("*QUIT")
        self.TCP_close()
        print(self.__class__.__name__ + ' had been disconnected!')

########## --data parse for luna only -- ###############
    def data_pasre(self, command):
        return command.decode().replace("\x00",'')

########## --super class alternative method --- #######
#    def read(self):
#        '''
#        The Luna response time may larger than TCP time out time.
#        Luna will response a binary list with EOS "\x00". 
#        '''
#        data = TCP.read_raw(self)
#        while True:
#            try:
#                if len(data) <= 1 or data[-1]!=0:
#                    data += TCP.read_raw(self)
#                else:
#                    break
#                #return data    
#            except:
#                pass
#        return data       
    
    def query(self,cmd):
        '''query result from Luna'''
        cmd = str(cmd)+"\n"
        self.write(cmd)
#        time.sleep(0.5)
        data = self.read_raw()
        return data

    def inspection(self,command ="SYST:ERR?" ,exception = '0'):
        while True:
            try:
                Q = self.query(command)
                #print (type(Q))
                #print (Q)
                if self.data_pasre(Q) == exception:
                    break
                else:
                    print("--> Verifing, or use Ctrl+C to end this process.")
            except:
                pass


#################---Traffic analyser ---###############
    @property
    def deviceID(self):
        return self.query("*IDN?")
    def CLS(self):
        self.write("*CLS\n")
    
    def BERperLane(self, laneID=0):
        self.CLS()
        cmd = "LINS5:FETC:DATA:TEL:PATT:ERR:RATE? {0},BIT".format(laneID)
        data = self.query(cmd)
        data = float(data.decode().replace('\n',''))
        return data
    
    def CurrentBERState(self, lane=8):
        for i in range(8):
            print("Lane {0} BER = ".format(i), self.BERperLane(i))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        