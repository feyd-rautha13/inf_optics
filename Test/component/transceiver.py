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
import openpyxl
import numpy as np

class QSFPDD():
    '''
    Compatible with  QSFP-DD Common Management specification Rev 3.0
    '''
    def __init__(self, interface, card = 1, port = 8):
        '''
        initial QSFP-DD;
        dev as a groove Hal instance.
        '''
        self.card = card
        self.port = port
        self.dev = interface

    def reg_set(self, page = 0x00, offset = 0x00, value = 0x00):
        
        address = format(page*256+offset, '#06x')
        cmd = "hw {0} qsfp {1} ww {2} {3}".format(self.card, self.port, address, value)
        self.dev.write(cmd)
    
    def reg_get(self, page = 0x00, offset = 0x00, length = 128):
        
        address = format(page*256+offset, '#06x')
        
        cmd = "hw {0} qsfp {1} rr {2} {3}".format(self.card, self.port, address, length)
        
        self.dev.clear_buffer()
        self.dev.write(cmd)
        data = self.dev.read_raw().decode()
        data = re.split(r'\r|\n', data)
        data = [x for x in data if x != ''][1: length+1]
        data = [ x[-2:] for x in data]
        
        return data
    
    def bit_set_one(self, value, offset):
        '''
        offset >= 0
        '''
        value |= 1<<offset
        return value
    
    def bit_set_zero(self, value, offset):
        '''
        offset >= 0
        '''
        value &= ~(1<<offset)
        return value
    
    def bit_get(self, value, offset):
        '''
        offset >=0
        '''
        value = (value>>offset)&0x01
        return value
    
    def password_entry(self):
        self.reg_set(0,118,0x00)
        self.reg_set(0,119,0x00)
        self.reg_set(0,120,0x10)
        self.reg_set(0,111,0x11)
        self.dev.clear_buffer()

#Table-18 Table-19
#Table 8-2 CMIS4.0
    @property
    def ModState(self):
        self.dev.clear_buffer()
        data = int(self.reg_get(0,3,1)[0],16)
        data = (data>>1 & 0x07)
        
        if data==1:
            return 'Module LowPwr state'
        elif data == 2:
            return 'Module PwrUp state'
        elif data == 3:
            return 'Module Ready state'
        elif data == 4:
            return 'Module PwrDn state'
        elif data == 5:
            return 'Module Fault state'
        else:
            return 'Reserved'
        
#CMIS 3.0 Table 22 Module level Monitor
#CMIS 4.0 Table 8-6 Module Monitors
    @property
    def ModMonCaseTemp(self):
        '''
        later. 
        '''
        self.dev.clear_buffer()
        data = self.reg_get(0,14,2)      
        data = (int(data[0],16)*256+int(data[1],16))/256
        if data<127:
            return data 
        else: 
            return data-127
    
    @property
    def ModMonInpVcc(self):
        self.dev.clear_buffer()
        data = self.reg_get(0,16,2)
        data = (int(data[0],16)*256+ int(data[1],16))*100/1E6
        
        return data        
        
    @property
    def ModMonLasTemp(self):
        self.dev.clear_buffer()
        data = self.reg_get(0,20,2)
        data = (int(data[0],16)*256+ int(data[0],16))/256
        if data<127:
            return data    
        else: 
            return data-127    
#Table 27
    @property
    def ModVendorName(self):
        self.dev.clear_buffer()
        s = ''
        data = self.reg_get(0,129,16)
        data = [chr(int(x,16)) for x in data]
        for i in data:
            s +=i
        return s
    
    @property
    def ModVendorPN(self):
        self.dev.clear_buffer()
        s = ''
        data = self.reg_get(0,148,16)
        data = [chr(int(x,16)) for x in data]
        for i in data:
            s +=i
        return s        
    
    @property    
    def ModVendorSN(self):
        self.dev.clear_buffer()
        s = ''
        data = self.reg_get(0,166,16)
        data = [chr(int(x,16)) for x in data]
        for i in data:
            s +=i
        return s       
    
    @property    
    def ModVendorSN2(self):
        self.dev.clear_buffer()
        s = ''
        data = self.reg_get(0,196,16)
        data = [chr(int(x,16)) for x in data]
        for i in data:
            s +=i
        return s    
        
    @property    
    def ModDateCode(self):
        self.dev.clear_buffer()
        s = ''
        data = self.reg_get(0,182,8)
        data = [chr(int(x,16)) for x in data]
        for i in data:
            s +=i
        return s        
        
#Table 31        
    @property
    def ModCableLength(self):
        self.dev.clear_buffer()
        data = int(self.reg_get(0,202,1)[0],16)
        multiplier = (data & 0xC0)>>5
        baselength = data & 0x1F
        
        if multiplier==0:
            return baselength*0.1
        elif multiplier == 1:
            return baselength*1
        elif multiplier == 2:
            return baselength*10
        elif multiplier == 3:
            return baselength*100
        else:
            return 'Reserved'        
        
#Table 32         
    @property
    def ModMediaType(self):
        self.dev.clear_buffer()

        data = self.reg_get(0,203,1)[0]

        return data   

#Module Infomation
    def ModInfo(self):
        self.dev.clear_buffer()
        print("Vendor Name\t",self.ModVendorName)
        print("Vendor PN\t", self.ModVendorPN)
        print("Vendor SN\t",self.ModVendorSN)
        print("Vendor Date\t",self.ModDateCode)

#CRC code
    def GetEEpromString(self, path, sh_order):
        wb = openpyxl.load_workbook(path)
        sheet = wb[wb.sheetnames[sh_order]]
        s=[]
        string = ''
        for i in range(2,120):
            addr = 'G'+str(i)
            s.append(str(sheet[addr].value))
            for i in s:
                string += i
                wb.close()
        return string
    
    def ModGetEEpromString(self):
        self.dev.clear_buffer()
        data1 = self.reg_get(0x03, 128, 120)
        data2 = data1.copy()
        del(data2[-2:])
        
        s1 = data1[-1]
        s2 = data1[-2]
        
        raw1 = ''
        raw2 = ''
        
        for i in data1:
            raw1 += i
        for i in data2:
            raw2 += i
        totaldata = raw2 + s1 + s2
        
        return raw1, raw2, totaldata
        
    
    def GenCRCCode(self, data):
        length = int(len(data)/2)
        crc = 0xffff
        for i in range(length):
            flag = int(data[2*i:2*i+2],16)
            crc ^= flag
            for i in range(8):
                last = crc%2
                crc >>= 1
                if last==1:
                    crc ^= 0xa001
        return hex(crc)
    
    def CRCcheck(self, data):
        eeprom = self.reg_get(0,128,117)
        s=''
        for i in eeprom:
            s += i
        return s
    
    def CRCcheck_infinera(self):
        data = self.ModGetEEpromString()[2]
        result = self.GenCRCCode(data)
        if result == '0x0':
            print('Pass')
        else:
            print('Fail!')

#Table 54
    @property
    def ModDisableAllLaser(self):
        self.dev.clear_buffer()
        self.reg_set(0x10, 130,0xFF)
    @property
    def ModEnableAllLaser(self):
        self.dev.clear_buffer()
        self.reg_set(0x10, 130,0x0)
    
    def ModEnSingleLane(self, lane):
        '''
        lane = 1:8
        '''
        self.dev.clear_buffer()
        cmd = 0xFF ^ (1<<(lane-1))
        self.reg_set(0x10,130, cmd)

#CMIS 3.0 Table 68
#CMIS 4.0 Table 8-60 Tx Flags
    def ModMonTxFault(self, lane):
        '''
        Lane 1:8
        '''
        self.dev.clear_buffer()
        data = int(self.reg_get(0x11, 135, 1)[0],16)
        data = self.bit_get(data, lane-1)
        return data

    def ModMonTxLos(self, lane):
        '''
        Lane 1:8
        '''
        self.dev.clear_buffer()
        data = int(self.reg_get(0x11, 136, 1)[0],16)
        data = self.bit_get(data, lane-1)
        return data
    
    def ModMonTxCDRLoL(self, lane):
        '''
        Lane 1:8
        '''
        self.dev.clear_buffer()
        data = int(self.reg_get(0x11, 137, 1)[0],16)
        data = self.bit_get(data, lane-1)
        return data


#CMIS 3.0 Table 69
#CMIS 4.0 Table 8-61 Rx Flags
    def ModMonRxLos(self, lane):
        '''
        Lane 1:8
        '''
        self.dev.clear_buffer()
        data = int(self.reg_get(0x11, 147, 1)[0],16)
        self.dev.clear_buffer()
        data = int(self.reg_get(0x11, 147, 1)[0],16)
        data = self.bit_get(data, lane-1)
        return data
    
    def ModMonRxCDRLoL(self, lane):
        '''
        Lane 1:8
        '''
        self.dev.clear_buffer()
        data = int(self.reg_get(0x11, 148, 1)[0],16)
        self.dev.clear_buffer()
        data = int(self.reg_get(0x11, 148, 1)[0],16)
        data = self.bit_get(data, lane-1)
        return data        
        

#CMIS 3.0 Table 70
#CMIS 4.0 Table 8-62        
    def ModMonTxPwr(self,Lane):
        '''
        Lane 1:8
        '''
        self.dev.clear_buffer()
        data = self.reg_get(0x11, 154+2*(Lane-1) ,2)
        data = (int(data[0],16)*256+ int(data[0],16))*0.1/1000
        data = 10*np.log10(data)
        
        return data
    
    def ModMonTxBias(self,Lane):
        '''
        Lane 1:8
        '''
        self.dev.clear_buffer()
        data = self.reg_get(0x11, 170+2*(Lane-1) ,2)
        data = (int(data[0],16)*256+ int(data[0],16))*2/1000
        
        return data
    
    def ModMonRxPwr(self,Lane):
        '''
        Lane 1:8
        '''
        self.dev.clear_buffer()
        data = self.reg_get(0x11, 186+2*(Lane-1) ,2)
        data = (int(data[0],16)*256+ int(data[0],16))*0.1/1000
        data = 10*np.log10(data)
        
        return data
        

###############---Innolight SSPRQ---##############
    def ModSSPRQ_Innolight(self):
        self.dev.clear_buffer()
        self.reg_set(0, 39, 0x01)
        self.reg_set(0, 37, 0xCC)
        
        self.reg_set(0,122, 0xCA)
        self.reg_set(0,123, 0x2D)
        self.reg_set(0,124, 0x81)
        self.reg_set(0,125, 0x5F)
        
        self.reg_set(129, 136, 0x85)
        self.reg_set(129, 137, 0)
        self.reg_set(129, 128, 0)
        self.reg_set(129, 129, 0x1E)
        self.reg_set(129, 130, 0x43)
        self.reg_set(129, 131, 0x9C)
        self.reg_set(129, 132, 0x02)
        self.reg_set(129, 133, 0x40)
        self.reg_set(129, 134, 0x03)

#################--CMIS4.0 SSPRQ--##############
    def ModMediaPG_CMIS4(self, pattern = 0x0C):
        self.dev.clear_buffer()
        '''
        Pattern generator.
        0: PRBS31Q, 2: PRBS23Q, 4:PRBS15Q, 6:PRBS13Q, 8:PRBS9Q, 10:PRBS7Q
        12: SSPRQ
        '''
        pattern = pattern<<4 + pattern
        self.reg_set(0x13, 156, pattern)
        self.reg_set(0x13, 157, pattern)
        self.reg_set(0x13, 158, pattern)
        self.reg_set(0x13, 159, pattern)
        
        self.reg_set(0x13, 152, 0xFF)
    
    def ModHostPG_CMIS4(self, pattern = 6):
        self.dev.clear_buffer()
        '''
        Pattern generator.
        0: PRBS31Q, 2: PRBS23Q, 4:PRBS15Q, 6:PRBS13Q, 8:PRBS9Q, 10:PRBS7Q
        12: SSPRQ
        '''

        pattern = pattern<<4 + pattern
        self.reg_set(0x13, 148, pattern)
        self.reg_set(0x13, 149, pattern)
        self.reg_set(0x13, 150, pattern)
        self.reg_set(0x13, 151, pattern)
        
        self.reg_set(0x13, 144, 0xFF)

    def ModMediaCheckerSet_CMIS4(self, pattern = 6):

        self.dev_clear_buffer()
        '''
        Pattern generator.
        0: PRBS31Q, 2: PRBS23Q, 4:PRBS15Q, 6:PRBS13Q, 8:PRBS9Q, 10:PRBS7Q
        12: SSPRQ
        '''

        pattern = pattern<<4 + pattern
        self.reg_set(0x13, 164, pattern)
        self.reg_set(0x13, 165, pattern)
        self.reg_set(0x13, 166, pattern)
        self.reg_set(0x13, 167, pattern)

        #Enable checker
        self.reg_set(0x13, 168, 0xFF)

##CMIS4.0 Table 8-93 Table 8-94
    def ModeMediaBER_CMIS4(self):

        self.dev_clear_buffer()

        #Enable selector
        self.reg_set(0x14, 128, 1)

        data = self.reg_get(0x14, 208, 8 )

        #BER calculation
        s0 = (data[0]&0xF8)>>3
        m0 = (data[0]&(0x7))<<8 + data[1]

        s1 = (data[2]&0xF8)>>3
        m1 = (data[2]&(0x7))<<8 + data[3]

        s2 = (data[4]&0xF8)>>3
        m2 = (data[4]&(0x7))<<8 + data[5]

        s3 = (data[6]&0xF8)>>3
        m3 = (data[6]&(0x7))<<8 + data[7]


        return m0*(10**(s0-24)), m1*(10**(s1-24)), m2*(10**(s2-24)), m3*(10**(s3-24))


        
class QSFP28():
    '''
    Compatible with  SFF-5636 Rev 2.9
    '''
    def __init__(self, interface, card = 1, port = 8, cardtype=0):
        '''
        initial QSFP-28;
        dev as a groove Hal instance.
        cardype:
            0: CHM2/CHM2T
            1: CHM1
        '''
        self.card = card
        self.port = port
        self.dev = interface
        self.cardtype = cardtype
    def reg_set(self, page = 0x00, offset = 0x00, value = 0x00):
        
        address = format(page*256+offset, '#06x')
        if self.cardtype==0:
            cmd = "hw {0} qsfp {1} ww {2} {3}".format(self.card, self.port, address, value)
        elif self.cardtype == 1:
            cmd = "hw {0} qsfp28 {1} ww {2} {3}".format(self.card, self.port, address, value)
        else:
            pass
        
        self.dev.write(cmd)
    
    def reg_get(self, page = 0x00, offset = 0x00, length = 128):
        
        address = format(page*256+offset, '#06x')
        if self.cardtype==0:
            cmd = "hw {0} qsfp {1} rr {2} {3}".format(self.card, self.port, address, length)
        elif self.cardtype == 1:
            cmd = "hw {0} qsfp28 {1} rr {2} {3}".format(self.card, self.port, address, length)
        else:
            pass
        
        self.dev.clear_buffer()
        self.dev.write(cmd)
        data = self.dev.read_raw().decode()
        data = re.split(r'\r|\n', data)
        data = [x for x in data if x != ''][1: length+1]
        data = [ x[-2:] for x in data]
        
        return data
    
    def bit_set_one(self, value, offset):
        '''
        offset >= 0
        '''
        value |= 1<<offset
        return value
    
    def bit_set_zero(self, value, offset):
        '''
        offset >= 0
        '''
        value &= ~(1<<offset)
        return value
    
    def bit_get(self, value, offset):
        '''
        offset >=0
        '''
        value = (value>>offset)&0x01
        return value
    #####################################################
    # Table 6-16
    @property
    def ModVendorPN(self):
        self.dev.clear_buffer()
        s = ''
        data = self.reg_get(0,168,16)
        data = [chr(int(x,16)) for x in data]
        for i in data:
            s +=i
        return s     

    ###################CRC check#########################
    def ModGetEEpromString(self):
        self.dev.clear_buffer()
        data1 = self.reg_get(0x02, 128, 120)
        data2 = data1.copy()
        del(data2[-2:])
        
        s1 = data1[-1]
        s2 = data1[-2]
        
        raw1 = ''
        raw2 = ''
        
        for i in data1:
            raw1 += i
        for i in data2:
            raw2 += i
        totaldata = raw2 + s1 + s2
        
        return raw1, raw2, totaldata
        
    
    def GenCRCCode(self, data):
        length = int(len(data)/2)
        crc = 0xffff
        for i in range(length):
            flag = int(data[2*i:2*i+2],16)
            crc ^= flag
            for i in range(8):
                last = crc%2
                crc >>= 1
                if last==1:
                    crc ^= 0xa001
        return hex(crc)

    
    def CRCcheck_infinera(self):
        data = self.ModGetEEpromString()[2]
        result = self.GenCRCCode(data)
        if result == '0x0':
            print('Pass')
        else:
            print('Fail!')
#################################################################