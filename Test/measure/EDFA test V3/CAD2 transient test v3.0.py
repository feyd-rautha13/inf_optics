# /usr/bin/env python
# -*- coding : utf-8 -*-

__author__ = 'Youbin Zheng'
__version__ = "2.1" 

'''
'''
import sys
import os
import time
import re
import math
import numpy as np
import pylab as plt
sys.path.append(".\\common_api") # ..
from datetime import datetime
from prologix import Prologix
#from ag8164b import AG8164B
#from ms9710b import MS9710B
from OSA_AQ6370 import AQ6370
#from osa_mts8000_api import OSA
from IQS import IQS
#from groove_api import HalAtGroove
#from common_api import getDspNameFromCard 
from SSHinterface import SSH
from SSHinterface import groove_cli
from SSHinterface import groove_Hal

def printLog(strings, returnMark=True):
	global GLB_LOG_FILE

	if returnMark ==True:
		print(strings, file=GLB_LOG_FILE)
		print(strings)
	else:
		print(strings, file=GLB_LOG_FILE)
		print(strings),
		
global GLB_LOG_FILE
if not os.path.exists(".\\results"):
		os.mkdir(".\\results")
GLB_LOG_FILE = open(".\\results\\tmpLog.log", 'w+')


###Groove init
#cli = groove_cli()
##hal = groove_Hal()
#cli.write("set amplifier-1/1.3/pa control-mode manual")
#cli.write("set cli-config interactive-mode disabled")
#cli.write('y')

hal = groove_Hal(host = '172.29.150.195', port = 8022, 
                 username = 'administrator' , password = 'e2e!Net4u#',
                 timeout = 10)


#hal.write("hw 1 ofp2 2 c x DoColdStart") 
#hal.write("hw 1 cpld x setOfp2Ctrl OFP2_2 MUTEL1 0")
hal.write("hw 1 cpld x setOfp2Ctrl OFP2_2 MUTEL2 0")
#hal.write("hw 1 cpld x setOfp2Ctrl OFP2_2 PUMPDIS1 0")
hal.write("hw 1 cpld x setOfp2Ctrl OFP2_2 PUMPDIS2 0")
#hal.write("hw 1 ofp2 2 c x SetEdfaEnable EDFA_1 1")
hal.write("hw 1 ofp2 2 c x SetEdfaEnable EDFA_2 1")
hal.write("hw 1 ofp2 2 x setPeriodActionStatus ALL_ACTION 0")
#hal.write("hw 1 ofp2 2 c x SetEdfaOperatingMode EDFA_1 AGC") 
hal.write("hw 1 ofp2 2 c x SetEdfaOperatingMode EDFA_2 AGC")
#hal.write("hw 1 ofp2 2 c x SetGainSetting EDFA_1 1000") 
hal.write("hw 1 ofp2 2 c x SetGainSetting EDFA_2 1000")
hal.read_raw()
time.sleep(1)
 
hal.write("hw 1 ofp2 2 c 1")
misc=hal.read_raw().decode('utf-8','ignore')
Vendor=re.findall(r"Vendor     = (.+) \r\n", misc)
SN=re.findall(r"Vend SN    = (.+)\r\n", misc)
Vendor=re.sub("\s","",Vendor[0])
SN=re.sub("\s","",SN[0])

HW=re.findall(r"HW Rev     = (.+)\r\n", misc)
HW=re.sub("\s","",HW[0])
FW=re.findall(r"FW Rev     = (.+)\r\n", misc)
FW=re.sub("\s","",FW[0])



curTime = datetime.utcnow().strftime("%Y%m%d%H%M")
startTime = time.time()
logPath = ".\\results\\{0}_{1}_{2}_{3}".format("Transient_CAD2",Vendor,SN,curTime)
#logPath = ".\\results\\{0}_{1}_{2}_{3}".format("Steady_BAX",,curTime)

os.mkdir(logPath)

###IQS init
iqs = IQS(host = '172.29.150.47', port = '5024', username=None, password=None)
printLog(iqs.read_raw())
iqs.write("KILL LINS10")
iqs.write("KILL LINS11")
iqs.write("KILL LINS12")
iqs.write("KILL LINS13")
iqs.write("KILL LINS14")
iqs.write("KILL LINS17")
iqs.write("CONNECT LINS10")
iqs.write("CONNECT LINS11")
iqs.write("CONNECT LINS12")
iqs.write("CONNECT LINS13")
iqs.write("CONNECT LINS14")
iqs.write("CONNECT LINS17")

iqs.write("LINS13:ROUT:SCAN 1")
iqs.write("LINS14:ROUT:SCAN 1")
iqs.write("LINS17:ROUT:SCAN 3")

iqs.write("LINS10:INP:ATT 10 DB")   
iqs.write("LINS11:ROUT:SCAN 1")
iqs.write("LINS12:ROUT:SCAN 1")
printLog(iqs.read_raw())
time.sleep(20)  #time adjust to activate the IQS


### test cases
#Pcal=11.12 # EDFA input power
Pcal=9.1
AttList=[]

#Pin=[-7, -13, -19]
#Gain=[10, 16, 22]

Pin=[8, -6]
Gain=[10, 24]

for i in range(2):
#for i in range(len(Pin)):
    print("Start Testing Case #" +str(i)+" ...")
    G_cmd="hw 1 ofp2 2 c x SetGainSetting EDFA_2 " + str(Gain[i]*100)

    #G_cmd="set amplifier-1/1.3/pa target-gain " + str(Gain[i]*10)
    hal.write(G_cmd)
    #hal.write("hw 1 ofp2 2 c x SetTilt EDFA_2 0")

    time.sleep(1)
    
        ####Switch to b2b

#    iqs.write("LINS11:ROUT:SCAN 2")
#    iqs.write("LINS12:ROUT:SCAN 2")
    
    Att=(Pcal-Pin[i])+0.579
    #Att=0.58 #for cal only
    #AttList.append(Att)
    Att_cmd="LINS10:INP:ATT " + str(Att)+ " DB"
    iqs.write(Att_cmd)
    #hal.write("hw 1 ofp2 2 c x DoColdStart") 
    time.sleep(1)
    #iqs.write("LINS10:INP:ATT 5 DB")

    input("Confirm Testing Case #" +str(i)+", then press <Enter>")
       

iqs.close()
hal.SSH_close()
#osa.close()
   
costTime = (time.time() - startTime) / 60
printLog("Cost time = {0}mins".format(str(costTime)))
#printLog("FW Rev = {0}".format(str(FW)))
#printLog("HW Rev = {0}".format(str(HW)))
printLog("")

	# change the raw file name with new information
GLB_LOG_FILE.close()
os.rename(".\\results\\tmpLog.log", logPath+"\\printLog.log") 
