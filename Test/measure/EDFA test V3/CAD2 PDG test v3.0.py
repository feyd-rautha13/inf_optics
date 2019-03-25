# /usr/bin/env python
# -*- coding : utf-8 -*-

__author__ = 'Youbin Zheng'
__version__ = "3.0"

'''
'''
import sys
import os
import time
import re
import numpy as np
import pylab as plt
sys.path.append(".\\common_api") # ..
from datetime import datetime
from prologix import Prologix
#from ag8164b import AG8164B
#from ms9710b import MS9710B
#from AQ6317 import AQ6317
#from osa_mts8000_api import OSA
from hp8152A import HP8152A
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

curTime = datetime.utcnow().strftime("%Y%m%d%H%M")
startTime = time.time()
logPath = ".\\results\\{0}_{1}_{2}_{3}".format("PDG_EDFA2",Vendor,SN,curTime)
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

iqs.write("LINS10:INP:ATT 1 DB")
iqs.write("LINS11:ROUT:SCAN 1")
iqs.write("LINS12:ROUT:SCAN 1")
iqs.write("LINS13:ROUT:SCAN 2")
iqs.write("LINS14:ROUT:SCAN 2")
iqs.write("LINS17:ROUT:SCAN 2")
time.sleep(30)

### Power meter init
host = "172.29.150.126"
port = 1234
PM_addr = 22
prologix = Prologix(host, port)
PM = HP8152A(PM_addr, prologix)
#PM.write("*RST")
time.sleep(1)
printLog(PM.deviceID)

### test cases
#Pcal=11.12 # EDFA input power
Pcal=11.05
AttList=[]
#Pin=[-10, -13, -16, -19, -22, 11.3, 8.3, 5.3, 2.3,-0.7]
#Gain=[10, 13, 16, 19, 22, 10, 13, 16, 19, 22]

##AGC mode
Pin=[-12, 8, -26, -6]
Gain=[10, 10, 24, 24]
#Pin=[-14, 7, -28, -7]
#Gain=[10, 10, 24, 24]
Count=range(60)
for i in range(4):
#for i in range(len(Pin)):
    print("Starting AGC Test Case # " +str(i)+"...")
    G_cmd="hw 1 ofp2 2 c x SetGainSetting EDFA_2 " + str(Gain[i]*100)

    #G_cmd="set amplifier-1/1.3/pa target-gain " + str(Gain[i]*10)
    hal.write(G_cmd)
    #time.sleep(1)
  
    Att=(Pcal-Pin[i])+0.579
    #Att=0.58 #for cal only
    #AttList.append(Att)
    Att_cmd="LINS10:INP:ATT " + str(Att)+ " DB"
    iqs.write(Att_cmd)
    time.sleep(2)
   
    PoutList=[]
   
    j=0
    for j in range(len(Count)):
        Pout=PM.power
        Pout=Pout+1.64 #calibration offset
        printLog(Pout)
        PoutList.append(Pout)
        time.sleep(1)
    GS=max(PoutList)-min(PoutList)      
           
    ###data saving

    fig = plt.figure(figsize=(8, 6))
    plt.plot(Count, PoutList, 'o-')
    plt.ticklabel_format(axis='y', style='sci', scilimits=(-2,2))
    plt.xlabel("Count")
    plt.ylabel("Pout")
    plt.grid()
    plt.savefig(logPath+"\\{0}_G{1}_P{2}.png".format("AGC",Gain[i],Pin[i]), format='png', dpi=96)
    
    curTime = datetime.utcnow().strftime("%Y%m%d%H%M")
    f = open(logPath+"\\PDG_test_data.log", "a+")
    print ("SUMMARY RESULTS:",file=f)
    print ("======================",file=f)
    print ("Gain (dB)	{0}".format(Gain[i]),file=f)
    print ("Input Power (dBm)	{0}".format(Pin[i]),file=f)
    print ("----------------",file=f)
    print ("PDG (dB)	{0}	{1}".format(GS,"+/-0.3dB"),file=f)
    print ("----------------",file=f)
    print ("{0}	{1}".format("Count","Pout"), file=f)
    for j in range(len(PoutList)):
    	print ("{0}	{1}".format(Count[j],PoutList[j]), file=f)
    f.close()

iqs.close()
hal.SSH_close()
#osa.close()
   
costTime = (time.time() - startTime) / 60
printLog("Cost time = {0}mins".format(str(costTime)))
printLog("")

	# change the raw file name with new information
GLB_LOG_FILE.close()
os.rename(".\\results\\tmpLog.log", logPath+"\\printLog.log") 
