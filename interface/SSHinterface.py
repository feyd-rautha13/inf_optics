# /usr/bin/env python
# -*- coding : utf-8 -*-

"""
Created on Thu Nov 15 15:06:32 2018
Modified on 
File description: SSH interface for groove

2018/12/21
change init function to super()
add pilot tone card support
    
"""

__author__ = 'Sizhan Liu'
__version__ = "1.0"


import paramiko
import time
import pprint
import re
import numpy as np

class SSH(object):
    def __init__(self, hostname='172.29.150.195', port = 8022, 
                 username = 'administrator' , password = 'e2e!Net4u#',
                 timeout = 10
                 ):
        self._host = hostname
        self._port = port
        self._username = username
        self._password = password

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            self.ssh.connect(self._host, self._port , self._username, self._password)
        except:
            data = self.__class__.__name__
            pprint.pprint(data + " "+ "connection failed!")
                

        self.shell = self.ssh.invoke_shell()
    
    def SSH_close(self):
        self.ssh.close()
        print(self.__class__.__name__ + ' connection is closed.')
    
    def write(self, command):
        command = str(command)+'\n'
        self.shell.send(command)
        time.sleep(0.5)
    
    def read_raw(self, buffer_size = 256):
        data = b''
     
        try:
            while self.ready_to_read():
                data = data + self.shell.recv(buffer_size)
            return data
        except:
            print('no more data')
    
    def ready_to_read(self):
        return self.shell.recv_ready()
    
    def clear_buffer(self):
        if self.ready_to_read() == True:
            self.read_raw()
        else:
            pass
    
    def inspection(self, section):      
        data = self.read_raw().decode()
 
        if section in data:
            return True
        else:
            return False

   
class groove_cli(SSH):
    def __init__(self, host = '172.29.150.195',
                 port = 8022, username = 'administrator' , password = 'e2e!Net4u#',
                 timeout = 10):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._timeout = timeout
        
        self._ssh_prompt = '~$ '
        self._cli_prompt = '> '
            
        super().__init__(self._host, self._port, self._username, self._password, self._timeout)
        time.sleep(2)
        
        if self.inspection(self._ssh_prompt):
            print('ssh connection successful!')
        else:
            print('ssh connection failed!')
            
        
        self.clear_buffer()
        self.write('\n')
        self.write("client")
        
        if self.inspection(self._cli_prompt):
            print ('Login to Groove CLi successful!')
        else:
            print('login failed!')
    
    def close_session(self):
        '''
        close ssh connection
        '''
        self.SSH_close()
        
    
    def cli_interactive_mode(self, cmd = 'disabled'):
        cmd = "set cli-config interactive-mode " + cmd
        self.clear_buffer()
        self.write(cmd)
        self.write('y')
    
    @property
    def show_inventory(self):
        '''
        show inventory
        '''
        self.clear_buffer()
        self.write('show inventory')
        invenroty = self.read_raw().decode()
        print (invenroty)
        
class groove_Hal(SSH):
    def __init__(self, host = '172.29.150.195',port = 8022, 
                 username = 'administrator' , password = 'e2e!Net4u#',
                 timeout = 10):
        
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._timeout = timeout
        
        self._ssh_prompt = '~$'
        self._hal_prompt = '/home/administrator# '
        self._hal_prompt_2 = 'HAL>'
        self._hal_username = 'su'
        self._hal_password = 'cosh1$'
        self._hal_path = 'cd /usr/local/bin'
        self._hal_paht_2 = './HAL'
        
        print('start to connect to server..')
        super().__init__(self._host, self._port, self._username, self._password, 
             self._timeout) 
        
        time.sleep(1)

        if self.inspection(self._ssh_prompt):
            print('ssh connection successful!')
        else:
            print('ssh connection failed!')
            self.close_session()
        
        time.sleep(0.5)
        print ('start to connect to HAL.')
        self.write('\n')
        
        self.write(self._hal_username)
        
        if self.inspection('Password'):
            print('enter password now..')
        else:
            pass
        
        self.write(self._hal_password)
        time.sleep(0.5)
        if self.inspection(self._hal_prompt):
            print ('Login in super user successfull.')
        else:
            print('Fail!')
        
        self.write(self._hal_path)
        time.sleep(1)
        self.write(self._hal_paht_2)
        time.sleep(1)
        self.write('\n')
        if self.inspection(self._hal_prompt_2):
            print ('Login HAL successfull!')
        else:
            print('Fail!')

            
    def close_session(self):
        '''
        close ssh connection
        '''
        self.SSH_close()

class O2OPT():
    def __init__(self, interface, card = 1, slot = 1,):
        self.card = card
        self.slot = slot
        self.dev = interface

 
    def get_fpga(self, address, area = 0):
        '''
        read memory map FPGA_uP area
        '''
        memory_map={
                0:'FPGA_uP',
                1:'DSP'
                }
        
        if area == 0:
            memory_area = memory_map[0]
            respond_tmp = 'READ FPGA-uP [{0}]: '.format(address)
        elif area == 1:
            memory_area = memory_map[1]
            respond_tmp = 'READ DSP [{0}]: '.format(address)
        else:
            print("Wrong input!")
        
        cmd = "hw {0} ofp2 {1} c x IndirectAccess {2} READ {3} 0x0".format(self.card, 
                  self.slot, memory_area ,hex(address))
        
        self.dev.write(cmd)
        data = self.dev.read_raw().decode()
        data = re.split(r'\r|\n', data)
        data = [x for x in data if x != '']
        
        data = int(data[1].replace(respond_tmp, ""),16)
        
        if area == 0:
            return hex(data)
        elif area == 1:
            return data
        else:
            return -1
            
    
    def set_fpga(self, address, value, section = 0):
        '''
        set memory map FPGA_uP area.
        address: DAC address
        cmd : operating number, Hex is better
        section: 
            0 total register operation
            1 MSB operation [27:16]
            2 LSB operation [11:0]
        '''
        memory_area = 'FPGA_uP'
        cmd = "hw {0} ofp2 {1} c x IndirectAccess {2} WRITE {3} ".format(self.card, 
                  self.slot, memory_area ,address)   
        data = int(self.get_fpga(address),16)
       
        if section == 0:
            value = value
            self.dev.write(cmd+str(value))
        elif section ==1:
            value = value<<16 | (0x000FFFF & data)
            self.dev.write(cmd+str(value))
        elif section == 2:
            value = value | (0xFFF0000 & data)
            self.dev.write(cmd+str(value))
        else:
            print('Wrong input!')
        
        #clear buffer
        self.dev.clear_buffer()
    
    def set_DSP(self, address, value):
        memory_area = 'DSP'
        cmd = "hw {0} ofp2 {1} c x IndirectAccess {2} WRITE {3} {4}".format(self.card, 
                  self.slot, memory_area ,address, value)
        self.dev.write(cmd)
        self.dev.clear_buffer()
        
    def ctrloop_SW_off(self):
        number=[9,19,29,39,49,59,69]
        for i in number:
            cmd = "hw {0} ofp2 {1} c x IndirectAccess CTRLOOP WRITE {2} 0".format(self.card, 
                  self.slot, i)
            self.dev.write(cmd)
            time.sleep(1)
            self.dev.clear_buffer()
    
    def dac_cfm(self):
        cmd = "hw {0} ofp2 {1} c x IndirectAccess FPGA_uP WRITE 0x303 0x1".format(self.card, 
                  self.slot)
        self.dev.write(cmd)
        self.dev.clear_buffer()
        
    def get_MR_status(self):
        data = self.get_fpga(0x801)
        return data
    
    def set_MR(self, MR_type = 0, MR_switch = 0):
        '''
        MR_type:
            0 working [7:0]
            1 protect [15:8]
        MR_switch:
            0 Gain 19.37
            1 Gain 1
            2 Gain 1
            3 Gain 1
        '''
        mr_status = int(self.get_MR_status(),16)
        value = 0
        switch = 0

        if MR_switch == 0:
            switch = 0x30
        elif MR_switch == 1:
            switch = 0x34
        elif MR_switch == 2:
            switch = 0x36
        elif MR_switch == 3:
            switch = 0x3F
        else:
            print('Wrong input!')
        
        if MR_type == 0:
            #working [7:0]
            value = (0xFF00 & mr_status) | switch

        elif MR_type == 1:
            #protect [15:8]
            value = (0x00FF & mr_status) | (switch<<8)            
        else:
            print('Wrong input!')
        
        cmd = "hw {0} ofp2 {1} c x IndirectAccess FPGA_uP WRITE 0x800 {2}".format(self.card, 
                  self.slot, value)
        self.dev.write(cmd)
        self.dev.clear_buffer()
        
    def get_Tone_freq(self):
        '''
        switch:
            0 Tx tone frequecny
            1 Rx working tone frequency
            2 Rx protect tone frequecny  
        unit Hz
        '''
        freq = []
        case = ('PT_GetFacTxToneFreq_1', 'PT_GetWorkRxToneFreq_1', 'PT_GetProtRxToneFreq_1')

        for i in case:
            cmd = "hw {0} ofp2 {1} c x {2}".format(self.card, self.slot, i)
            self.dev.write(cmd)
            data = self.dev.read_raw().decode()
            data = re.split(r'\r|\n', data)
            data = [x for x in data if x != '']
            data = int(data[1])
            freq.append(data)
        
        return freq
    
    def set_Tone_freq(self, switch = 0, freq = 1000):
        '''
        switch:
            0 Tx
            1 Rx working 
            2 Rx protect
        unit kHz
        '''

        if switch == 0:
            case = 'PT_SetFacTxToneFreq_1'
        elif switch == 1:
            case = 'PT_SetWorkRxToneFreq_1'
        elif switch == 2:
            case = 'PT_SetProtRxToneFreq_1'
        else:
            print('Wrong input!')
        
        cmd = "hw {0} ofp2 {1} c x {2} {3}".format(self.card, self.slot, case, freq)
        self.dev.write(cmd)
        self.dev.clear_buffer()
    
    def set_Tone_freq_manuel(self):
        cmd = "hw {0} ofp2 {1} x setPeriodActionStatus ALL_ACTION false".format(self.card, 
                  self.slot)
        self.dev.write(cmd)
        self.dev.clear_buffer()
        
    def adc_parse(self, data, level = 0):
        '''
        0: lsb
        1: msb
        '''
        if level == 0:
            data = data & 0x00000FFF
        elif level == 1:
            data = (data>>16) & 0x00000FFF
        else:
            print('Wrong input')
        return data
    
    def m_value_w(self, offsetRxWVgaGain = -227):
        if self.dev.ready_to_read():
            self.dev.clear_buffer()
        
        rx_pow_m = self.get_fpga(0x401)
        rx_pow_m_w = self.adc_parse(int(rx_pow_m,16), 0)
        
        gf4_pw = self.get_fpga(3,1)
        
        m_value = 83*(np.sqrt(gf4_pw)/10000)/(rx_pow_m_w/4096)/10**(offsetRxWVgaGain/1000)
        
        return m_value
        
        
        
            
            
            
            
            
            
