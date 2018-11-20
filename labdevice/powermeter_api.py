#-------------------------------------------------------------------------------
# Purpose:     Power Test in ShangHai Lab
#
# Author:      Youbin Zheng/Sizhan Liu
# Reference    Yingkan Chen's Prologix controller
# Version:     1.0  
#
# Created:     11/10/2016
# Modify:      11/07/2017
# Copyright:   (c) Coriant R&D GmbH 2016 
#-------------------------------------------------------------------------------


# System level import
import time
# site-package import
import socket
# 3rd party project module import
import re
# Project module import

#from abc import ABCMeta, abstractmethod

class Powermeter:

    def __init__(self, host, port, addr, sock = None):
    #def __init__(self, host = "10.13.11.59", port = 1234, addr = "11", sock = None):
    #def __init__(self, host = "172.29.150.126", port = 1234, addr = "22", sock = None):
        self.host_ = host
        self.port_ = port
        self.addr_ = addr
        self.logFile = "NA"
        self.printLog("Connecting to Powermeter...")
			
        if sock == None:
            # === Connect ===
            # Open TCP connect to poet 1234 of GPIB-ETHERNET
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
            self.sock.settimeout(5)
            self.sock.connect((self.host_, self.port_))

            # Set mode as CONTROLLER
            strtmp = "++mode 1\n"
            self.sock.send(strtmp.encode())

            # Set HP33120A address
            #strtmp = "++addr " + self.addr_ + "\n"
            strtmp = "++addr " + self.addr_ + "\n"
            self.sock.send(strtmp.encode())

            # Turn off read-after-write to avoid "Query Unterminated" errors
            strtmp = "++auto 0\n"
            self.sock.send(strtmp.encode())

            # Read timeout is 3000 msec --U.B. adjusted time out for 86120B
            strtmp = "++read_tmo_ms 3000\n"
            self.sock.send(strtmp.encode())

            # Do not append CR or LF to GPIB data
            strtmp = "++eos 3\n"
            self.sock.send(strtmp.encode())

            # Assert EOI with last byte to indicate end of data
            strtmp = "++eoi 1\n"
            self.sock.send(strtmp.encode())
        else:
            self.sock = sock

#    timeout = 3
#    for i in range(0, timeout):
#			try:
#				#self.setAddr()
#				self.reset()
#				ID=self.ask("*idn?")
#				if (ID):
#					self.printLog(ID)
#					break
#			except:
#				self.printLog("Error!! Connect to Wavemeter fail")
		

    def printLog(self, strings, returnMark=True):
        if returnMark ==True:
			if self.logFile != "NA":
				print >>self.logFile, strings
			print strings
        else:
			if self.logFile != "NA":
				print >>self.logFile, strings,
			print strings,

    def setAddr(self):
        #strtmp = "++addr " + self.addr_ + "\n"
        strtmp = "++addr " + self.addr_ + "\n"
        #print(strtmp)
        self.sock.send(strtmp.encode())

    def ask(self, cmd):
        while True:
            try:
                #time.sleep(1)
                self.setAddr()
                time.sleep(1)
                self.write(cmd)
                time.sleep(1)
                #time.sleep(.5)
                self.sock.send("++read eoi\n".encode())
                time.sleep(3) #solve data overlap issue 1->3->5
                #return self.sock.recv(1000)
                return self.sock.recv(1024)
            except:
                print('Recv timeout')
                #time.sleep(1)

    def write(self, cmd):
        self.setAddr()
        strtmp = cmd + "\n"
        self.sock.send(strtmp.encode())

    def close(self):
        print(self.__class__.__name__ + ' is closed.')
        self.sock.close()
    
    def reset(self):
		rst = self.write("*rst")
		return rst    

    def getID(self):
        ID = self.ask("*idn?")
        return ID
    
    def getPower(self):
		Power = self.ask("Pwmtr")
		Power=Power.replace("\r\n","")
		Power=float(Power)
		return Power  
#s.sock.send("++addr 11\n".encode())
#s.sock.send("*IDN?\n".encode())
#s.sock.send(":MEAS:SCAL:POW:WAV?".encode())

#s.sock.send("++read eoi\n".encode())
#s.sock.recv(1024)
