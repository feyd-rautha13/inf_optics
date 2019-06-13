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
    
    def password_entry(self):
        self.reg_set(0,118,0x00)
        self.reg_set(0,119,0x00)
        self.reg_set(0,120,0x10)
        self.reg_set(0,111,0x11)
        self.dev.clear_buffer()

#Table-18 Table-19   
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
        
#Table 22 Module level Monitor
    @property
    def ModMonCaseTemp(self):
        '''
        later. 
        '''
        self.dev.clear_buffer()
        data = self.reg_get(0,14,2)      
        data = (int(data[0],16)*256+int(data[1],16))/256
        if data<128:
            return data 
        else: 
            return data-128
    
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
        if data<128:
            return data    
        else: 
            return data-128    
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
    
    
    
    