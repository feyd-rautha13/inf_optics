# /usr/bin/env python
# -*- coding : utf-8 -*-

'''
Reversion history

Rev 1.0 Thu Mar-07-2019
Created.


File description: 
OFP2 card for groove
'''
__author__ = 'Sizhan Liu'
__version__ = "1.0"

class O2O1x4WSS():
    def __init__(self, interface, card = 1, slot = 1,):
        self.card = card
        self.slot = slot
        self.dev = interface

    def AddChn(self, ChnName = 'ch1', frequency = 191150, bw = 50):
        '''
        Add channel, center frequency and bandwidth.
        '''
        cmd = "hw {0} ofp2 {1} nmc add {2} {3} {4}".format(self.card, self.slot, ChnName, frequency*1000 ,bw*1000)
        self.dev.write(cmd)

    def AttSet(self, ChnName = 'ch1', value = 1):
        cmd = "hw {0} ofp2 {1} nmc atten {2} {3}".format(self.card, self.slot, ChnName, value*10)
        self.dev.write(cmd)

    def DelChn(self, ChnName = 'ch1'):
        '''
        Drop channel you had added.
        '''
        cmd = "hw {0} ofp2 {1} nmc del {2}".format(self.card, self.slot, ChnName)
        self.dev.write(cmd)

    def EnableChn(self, ChnName = 'ch1', port = 3):
        '''
        Operate WSS to enable channel link to the port you selected. 
        '''
        if port not in [0,1,2,3]:
            print ("wrong setting")
        cmd = "hw {0} ofp2 {1} nmc xc {2} {3} 1".format(self.card, self.slot, ChnName, port)
        self.dev.write(cmd)

    def DisChn(self, ChnName = 'ch1', port = 3):
        '''
        Operate WSS to disable channel link to the port you selected. 
        '''
        if port not in [0,1,2,3]:
            print ("wrong setting")
        cmd = "hw {0} ofp2 {1} nmc xc {2} {3} 0".format(self.card, self.slot, ChnName, port)
        self.dev.write(cmd)



