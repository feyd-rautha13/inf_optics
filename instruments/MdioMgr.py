#-------------------------------------------------------------------------------
# Name:        MdioMgr.py
# Purpose:     
#              
#
# Author:      Yingkan Chen
#
# Version:     
#
# Created:     12/10/2016
# Copyright:   (c) Coriant R&D GmbH 2016
#-------------------------------------------------------------------------------

# System level import
import time
import binascii
import sys,os


# site-package import
from socket import *

# 3rd party project module import

# Project module import


class MdioMgr:
    def __init__(self, host, port, slot, sled, LIM400 = 0, sock=None, aco_mdio=None):
        os.path.ab
        self.host = host
        self.port_ = port
        self.slot = slot
        self.sled = sled
        self.LIM400 = LIM400
        self.aco_mdio = aco_mdio

        if sock is None:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.settimeout(20)  # raise timeout exception after blocking 20 seconds
        else:
            self.sock = sock

    def connect(self):
        self.sock.connect((self.host, self.port_))

    def disconnect(self):
        self.sock.close()
        # self.sock = None

    def sendAddress(self, addr):
        packet = '\x76\x30\x30\x32\x00\x05\x00\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04' + chr(addr >> 8) + chr(addr & 0xff) + '\x00\x00'
        self.sock.send(str(packet))
        data = self.sock.recv(1024)

    def readMdioWord(self, addr):
        return self.readWord(addr)

    def readMeruRegister(self, addr):
        return self.readWord(addr)

    def readDenaliRegister(self, addr):
        return self.readWord(addr)

    def readCfp2Register(self, addr):
        if self.aco_mdio == None:
            return self.readWord(addr)
        else:
            return self.aco_mdio.readCfp2Register(addr)

    def readWord(self, addr):
        # Address phase
        self.sendAddress(addr)
        # Read phase
        packet = '\x76\x30\x30\x32\x00\x05\x00\x09\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04' + chr(addr >> 8) + chr(addr & 0xff) + '\x00\x00'
        self.sock.send(str(packet))
        data = self.sock.recv(1024)
        # Convert and return
        if len(data) < 28:
            raise Warning('runt response %d bytes 0x%s'
                          % (len(data), binascii.hexlify(data)))
        bdata = bytearray(data[26:])
        return (bdata[0] << 8 | bdata[1])

    def writeMdioWord(self, addr, value):
        self.writeWord(addr, value)

    def writeMeruRegister(self, addr, value):
        self.writeWord(addr, value)

    def writeDenaliRegister(self, addr, value):
        self.writeWord(addr, value)

    def writeCfp2Register(self, addr, value):
        # if '0x' in value:
        #     value = int(value, 16)

        if self.aco_mdio == None:
            self.writeWord(addr, value)
        else:
            self.aco_mdio.writeCfp2Register(addr, value)

    def blockReadCfp2Register(self, num_regs, first_reg_ad):
        addr, output = self.readBlock(first_reg_ad, num_regs)
        return addr, output

    def blockReadDenaliRegister(self, num_regs, first_reg_ad):
        addr, output =self.readBlock(first_reg_ad, num_regs)
        return addr, output

    def writeWord(self, addr, value):
        self.mdioRdy()
        # Address phase
        self.sendAddress(addr)
        # Write phase
        packet = '\x76\x30\x30\x32\x00\x05\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04' + \
                 chr(addr >> 8) + chr(addr & 0xff) + chr(value >> 8) + chr(value & 0xff)
        self.sock.send(str(packet))
        data = self.sock.recv(4096)
        #print('received!')
        # self.sock.send(str(packet))
        # data = self.sock.recv(1024)
        return

    # Check that the MDIO is ready for write
    def mdioRdy(self):
        for i in range(1, 10):
            mdio_rdy = self.readMdioWord(0xB050)
            if (mdio_rdy & 0x8000) == 0:
                time.sleep(1)
            else:
                break
        if i == 10:
            print("ERROR: Ready for write bit not ready")
            return
        return

    # Read 64 bit word
    def read64bit(self, addr):
        data = 0
        for i in range(4):
            data = data << 16 | self.readMdioWord(addr)
            addr += 1
        return data

    # Read 32 bit floating point value and convert it to integer
    def read32bitflp(self, addr):
        data = 0
        self.mdioRdy()
        data = self.readMdioWord(addr)
        return (data & 0x03FF) * 2 ** ((data & 0xFC00) >> 10)

    # Read 32 bit word
    def read32bit(self, addr):
        data = 0
        for i in range(2):
            data = data << 16 | self.readMdioWord(addr)
            addr += 1
        return data

    def writeBlock(self, addr, data):
        length = len(data) * 2 + 2
        packet = '\x76\x30\x30\x32\x00\x05\x00\xbb\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + chr(
            length >> 8) + chr(length & 0xff) + chr(addr >> 8) + chr(addr & 0xff)
        for i in range(len(data)):
            packet += chr((data[i] >> 8) & 0xff) + chr(data[i] & 0xff)
        self.sock.send(str(packet))
        data = self.sock.recv(1024)
        return

    def readBlock(self, addr, length):    # length: number of 16 bit words to read
        output = []
        addr_tmp = []
        for i in range(0,length ):
            addr_tmp.append(addr + i)
            output.append(self.readCfp2Register(addr + i))
        # Read phase
        # packet = '\x76\x30\x30\x32\x00\x05\x00\xAA\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04' + chr(addr>>8) + chr(addr&0xff) + chr(length>>8) + chr(length&0xff)
        # self.sock.send(str(packet))
        # data = self.sock.recv(2048)
        # # Convert and return
        # if len (data) <> (24 + 2 * length):
        #     raise Warning ('runt response %d bytes 0x%s' % (len(data), binascii.hexlify (data)))
        #
        # return bytearray(data[24:(24+2*length)])
        return addr_tmp, output


    def WaitForCdbIdle(self):
        oneMessage = True  # debug, can remove
        for i in range(0, 20):
            cmdReply = self.readMdioWord(0x9A00)
            # Check to make sure that the previous command is complete
            if (cmdReply == 0x0001):
                break
            if oneMessage:  # debug, can remove
                print "CDB interface not immediately idle"  # debug, can remove
                oneMessage = False  # debug, can remove
            time.sleep(0.1)
        if oneMessage == False:
            if i == 1:
                print "   -> 1 delay loop needed"
            else:
                print "   -> %d delay loops needed" % i
        if (cmdReply != 0x0001):
            print "CDB interface did not go to idle state!"
            return False
        return True

    def lowPowerHW(self):
        cmdReply = self.readMdioWord(0xB010)

        # Check if Soft module low power (0x4000) and/or MOD_LOPWR pin (0x0010) is asserted
        if ((cmdReply & 0x0010) != 0):
            print "Device is in low power mode (HW pin is asserted)! Please set it to high power before you can continue!"
            return True
        else:
            return False

    def writeHal(self,str):
        print('Not implemented')
        return 'NA'

    def get_card_sn(self):
        print('Not implemented')
        return 'NA'

    def readFanSpeed(self):
        print('Not implemented')
        return 'NA'

    def dumpStatus(self):
        print('Not implemented')
        return 'NA'

    def switchQefOnOff_wrapper(self, flag):
        print('Not implemented')
        return 'NA'

    def startBkgProcess(self):
        print('Not implemented')
        return 'NA'

    def closeBkgProcess(self):
        print('Not implemented')
        return 'NA'

    def startAllBkgProcess(self):
        print('Not implemented')
        return 'NA'

    def closeAllBkgProcess(self):
        print('Not implemented')
        return 'NA'

    def dumpLineInfo_wrapper(self):
        print('Not implemented')
        return 'NA'

    def setFanSpeed(self,val):
        print('Not implemented')
        return 'NA'

    def set_tx_pilot_symbol_ctrl(self, str1, st2):
        print('Not implemented')
        return 'NA'

    def set_rx_pilot_symbol_ctrl(self,str1, str2):
        print('Not implemented')
        return 'NA'

    def read_tx_pilot_symbol_ctrl(self):
        print('Not implemented')
        return 'NA'
