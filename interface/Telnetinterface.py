# /usr/bin/env python
# -*- coding : utf-8 -*-

"""
Created on Sat Nov 17 17:34:15 2018

Modified List: 
version 1.1 Sun Jun 30, 17:20, 2019

File description: Telnet basic
    
"""

__author__ = 'Sizhan Liu'
__version__ = "1.1"


import telnetlib
import time

class telnet(object):
    def __init__(self, host, port, timeout=5):
        
        self._host = host
        self._port = port
        self._timeout = timeout

        
        self.tn = telnetlib.Telnet()
        try:
            self.tn.open(self._host, self._port, self._timeout)
        except ConnectionError:
            print(self.__class__.__name__+ " connection failed!")
    
    def close_telnet(self):
        self.tn.close()
        print(self.__class__.__name__+ ' closed!')
        
    def write(self, cmd):
        self.clear_buffer()
        cmd = str(cmd) + '\n'
        cmd = cmd.encode()
        self.tn.write(cmd)
        
    def read_raw(self, prompt = '>'):

        prompt = prompt.encode()
        data = self.tn.read_until(prompt, timeout=10)
        return data

    
    def clear_buffer(self):
        try:
            while(self.tn.read_very_eager() != b''):
                time.sleep(0.01)
        except:
            pass
    
    def query(self, cmd, prompt = '>'):
        self.write(cmd)
        data = self.read_raw(prompt)
        
        return data
        
                
