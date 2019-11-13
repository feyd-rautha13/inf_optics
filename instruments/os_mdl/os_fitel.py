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
import socket
import time
import sys
# site-package import

# 3rd party project module import

# Project module import


class os_fitel:
    def __init__(self, host = "10.50.22.105", port = 1234, addr = "13", sock = None):
        self.host_ = host
        self.port_ = port
        self.addr_ = addr

        if sock == None:
            print('FITEL optcial switch init')
            # === Connect ===
            # Open TCP connect to poet 1234 of GPIB-ETHERNET
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
            self.sock.settimeout(5)
            self.sock.connect((self.host_, self.port_))

            # Set mode as CONTROLLER
            strtmp = "++mode 1\n"
            self.sock.send(strtmp.encode())

            strtmp = "++ifc\n"
            self.sock.send(strtmp.encode())

            # Set HP33120A address
            strtmp = "++addr " + self.addr_ + "\n"
            self.sock.send(strtmp.encode())

            # Turn off read-after-write to avoid "Query Unterminated" errors
            strtmp = "++auto 0\n"
            self.sock.send(strtmp.encode())

            strtmp = "++eoi 0\n"
            self.sock.send(strtmp.encode())

            strtmp = "++read eoi\n"
            self.sock.send(strtmp.encode())

            # Assert EOI with last byte to indicate end of data
            self.sock.send(("++eos 0\n").encode())
        else:
            self.sock = sock

        self.osIsRunning = True
        print('Optical switch init done')

    def setAddr(self):
        strtmp = "++addr " + self.addr_ + "\n"
        self.sock.send(strtmp.encode())

    def currClosedPort(self):
        self.setAddr()
        try:
            strtmp = "CLOSE?\n"
            self.sock.send(strtmp)
            self.sock.send("++read eoi\n")
            portClosed = str(self.sock.recv(1024))
            print(self.__class__.__name__  + ' read out %s'% portClosed)
            return [int(s) for s in portClosed.split() if s.isdigit()][0]
        except:
            print('+++' + self.__class__.__name__  + ' read out NaN+++')
            return 99

    def switch2Port(self, portNo):
        flag = True
        self.setAddr()
        strtmp = "CLOSE " + str(portNo) + "\n"
        self.sock.send(strtmp)
        time.sleep(2)

        while flag:
            portClosed = self.currClosedPort()
            # if "1" in portClosed and portNo == 1:
            #     print("+++Switch optical path to " +  str(portNo) + " succeeded.+++")
            #     print("Noise source is ON.")
            # elif "2" in portClosed and portNo == 2:
            #     print("+++Switch optical path to " + str(portNo) + " succeeded.+++")
            #     print("Signal source is ON.")
            # else:
            #     print("Something is wrong, please check the optical switch setup.")
            if portNo ==  portClosed:
                print("+++Switch optical path to " + str(portNo) + " succeeded.+++")
                break
            else:
                print("+++Switch failed+++")
                print("+++Retry to read the switch closed port+++")

    def disconnect(self):
        self.sock.close()

# def main(argv):
#     os_inst_ = os_fitel()
#     if argv == str(0): # Signal source
#         os_inst_.switch2Port(2)
#         print("+++FITEL optical switch should have signal source on the 2nd port+++")
#         print("Signal source is ON.")
#     elif argv == str(1): # Noise source
#         os_inst_.switch2Port(1)
#         print("+++FITEL optical switch should have noise source on the 1st port+++")
#         print("Noise source is ON.")
#     os_inst_.disconnection()

if __name__ == "__main__":
    # main(sys.argv[1])
    os_inst_ = os_fitel(host= '10.148.255.133', addr='13')
    # os_inst_ = os_fitel(host='10.50.18.26', addr='13')
    # os_inst_ = os_fitel(host='10.50.22.99', addr='20')
    os_inst_.switch2Port(7)
