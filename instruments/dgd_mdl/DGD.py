#-------------------------------------------------------------------------------
# Name:        cfp2aco_platform.py
# Purpose:     
#              
#
# Author:      Yingkan Chen
#
# Version:     
#
# Created:     11/10/2016
# Copyright:   (c) Coriant R&D GmbH 2016
#-------------------------------------------------------------------------------

# System level import
import time
# site-package import
import socket
# 3rd party project module import

# Project module import

from abc import ABCMeta, abstractmethod

class DGD:
    def __init__(self, host, port, addr, sock):
        self.host_ = host
        self.port_ = port
        self.addr_ = addr

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
            strtmp = "++addr " + self.addr_ + "\n"
            self.sock.send(strtmp.encode())

            # Turn off read-after-write to avoid "Query Unterminated" errors
            strtmp = "++auto 0\n"
            self.sock.send(strtmp.encode())

            # Read timeout is 200 msec
            strtmp = "++read_tmo_ms 200\n"
            self.sock.send(strtmp.encode())

            # Do not append CR or LF to GPIB data
            strtmp = "++eos 3\n"
            self.sock.send(strtmp.encode())

            # Assert EOI with last byte to indicate end of data
            self.sock.send(("++eos 0\n").encode())
        else:
            self.sock = sock

        self.voaIsRunning = True

    def setAddr(self):
        strtmp = "++addr " + self.addr_ + "\n"
        #print(strtmp)
        self.sock.send(strtmp.encode())

    def ask(self, cmd):
        while True:
            try:
                self.setAddr()
                self.write(cmd)
                time.sleep(.5)
                self.sock.send("++read eoi\n".encode())
                return self.sock.recv(1000)
            except:
                print('Recv timeout')
                time.sleep(5)

    def write(self, cmd):
        self.setAddr()
        strtmp = cmd + "\n"
        self.sock.send(strtmp.encode())

    def closeDGDConnection(self):
        print(self.__class__.__name__ + ' is closed.')
        self.sock.close()