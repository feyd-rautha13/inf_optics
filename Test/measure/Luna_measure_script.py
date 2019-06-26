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
    'host' : "10.13.11.254", 
    'port' : 1
    }


#Remote folder path
path = "C:\\Users\\lab\\Desktop\\New folder\\"
# device Descriptor
dutname = 'tt'

def test(filepath, dutname):
    #Luna initial
    astart = time.time()
    luna = Luna(ip['host'], ip['port'])

    #Test init
    luna.measType()   
    luna.measAverage(number = 10) 
    luna.measFindDutLength()
    
    #Apply Time domain filter, Remeber the current time domain filter
    luna.setTimeDomain()

    #set DUT name
    luna.setDUTName(dutname)
    #Start test
    luna.scan()
    
    time.sleep(2)
    
    #check if scan finished
    print(luna.query("*OPC?"))
    
    '''check if something wrong.''' 
    #print measurement information
    print("---------------- Measurement Detail ---------------")
    luna.measDetail()

    #luna.fetchresult()

    #File save
    #input("--> Press anykey to store data files..")
    filepath = filepath+dutname
    luna.savebinResult(filename=filepath)
    #print(luna.query("*OPC?"))
    luna.savetxtResult(filename=filepath)
    print(luna.query("*OPC?"))
    print("--> Test {0} Done!".format(dutname))
    
    #close connection
    luna.close()
    astop = time.time()
    print ("test time = ", astop - astart)



