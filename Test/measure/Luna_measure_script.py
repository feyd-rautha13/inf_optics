# /usr/bin/env python
# -*- coding : utf-8 -*-


__author__ = 'sizhan Liu'
__version__ = '1.0'

import sys
sys.path.append('D:\\work\\coding\\python\\inf_optics\\labdevice\\')

from ova5000 import Luna
import time

#device IP
ip = {
    'host' : "10.13.51.252", 
    'port' : 1
    }

#C band and C+L band test plan
testplan = {
    'center': {'C':1549.0,'C+L':1569.0},
    'range':{'C': 41.67,'C+L':85.69}
    }


def test():
    #Luna initial
    luna = Luna(ip['host'], ip['port'])

    #Test init
    luna.measType()   
    luna.measAverage(number = 10) 

    luna.measFindDutLength()
    
    #Test parameter 
    #should set start and range, center range would not affect test plan
    #startwav = 1527.38
    #luna.startWav = startwav

    #Luna.centerWav = testplan['center']['C']
    #luna.rangeWav = testplan['range']['C']

    #Apply filter
    luna.setSmoothFilter()
    luna.setTimeDomain()

    #set DUT name
    dutname = input("--> please enter dut name:")
    luna.setDUTName(dutname)
    #Start test
    luna.scan()

    #set smoothing filter to Matrix A
    luna.measApplyFilter()
    luna.setSmoothFiltertoMatirxA()
    
    time.sleep(5)
    print(luna.query("*OPC?"))
    
    '''check if something wrong.'''   
    luna.fetchresult()
    #print measurement information
    #print (luna.measInfor.decode().replace("\x00",""))

    #print measurement information
    #print('Device ID: ', luna.data_pasre(luna.deviceID))
    #print('Center Wavelength: ', luna.data_pasre(luna.centerWav))
    print('--> Start wavelength: ', luna.data_pasre(luna.startWav))
    #print('Scan Range: ', luna.data_pasre(luna.rangeWav))
    print('--> Stop wavelength: ', luna.data_pasre(luna.stopWav))
    #print('Firmware version: ', luna.data_pasre(luna.query("SYST:VER?")))
    #print('Start frequency and increasment: ', luna.data_pasre(luna.query(''"FETC:FREQ?")))
    #print('Time increasement: ', luna.data_pasre(luna.query("FETC:TINC?")))
    #print('Time domain window resolution bandwidth: ', luna.data_pasre(luna.query("CONF:TWRB?")))
    #print('Convolved Res BW: ', luna.data_pasre(luna.query("CONF:CRBW?")))
    #print('Sample resolution: ', luna.data_pasre(luna.query("CONF:SRES?")))
    #print('Time domain sigma', luna.data_pasre(luna.query("CONF:TSIG?")))
    #print('Time domain start / stop: ', luna.data_pasre(luna.query("CONF:TLIM?"))) #time domain start / stop
    #print('smoothing filter bandwidth unit', luna.data_pasre(luna.query("CONF:RSBU?"))) #smoothing filter bandwidth unit
    print('--> smoothing filter value', luna.data_pasre(luna.query("CONF:FRBW?"))) #smoothing filter value


    #File save
    #input("--> Press anykey to store data files..")
    filepath = "C:\\Data\\sliu3\\Documents\\work\\test\\P0\\mux\\"+dutname
    #luna.savebinResult(filename=filepath)
    #print(luna.query("*OPC?"))
    luna.savetxtResult(filename=filepath)
    print(luna.query("*OPC?"))
    
    #close connection
    #luna.close()


if __name__ == "__main__":
    astart = time.time()
    test()
    astop = time.time()
    
    print ("test time = ", astop - astart)





