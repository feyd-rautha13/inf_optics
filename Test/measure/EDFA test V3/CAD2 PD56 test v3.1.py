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

###Groove init
#cli = groove_cli()
##hal = groove_Hal()
#cli.write("set amplifier-1/1.3/pa control-mode manual")
#cli.write("set cli-config interactive-mode disabled")
#cli.write('y')
#cli.cli_interactive_mode
hal = groove_Hal(host = '172.29.150.195', port = 8022, 
                 username = 'administrator' , password = 'e2e!Net4u#',
                 timeout = 10)
#hal = groove_Hal()


#hal.write("hw 1 ofp2 2 c x DoColdStart") 
#hal.write("hw 1 cpld x setOfp2Ctrl OFP2_2 MUTEL1 0")
hal.write("hw 1 cpld x setOfp2Ctrl OFP2_2 MUTEL2 0")
#hal.write("hw 1 cpld x setOfp2Ctrl OFP2_2 PUMPDIS1 0")
hal.write("hw 1 cpld x setOfp2Ctrl OFP2_2 PUMPDIS2 0")
#hal.write("hw 1 ofp2 2 c x SetEdfaEnable EDFA_1 1")
hal.write("hw 1 ofp2 2 c x SetEdfaEnable EDFA_2 1") 
hal.write("hw 1 ofp2 2 c 1")
misc=hal.read_raw().decode('utf-8','ignore')
Vendor=re.findall(r"Vendor     = (.+) \r\n", misc)
SN=re.findall(r"Vend SN    = (.+)\r\n", misc)
Vendor=re.sub("\s","",Vendor[0])
SN=re.sub("\s","",SN[0])

curTime = datetime.utcnow().strftime("%Y%m%d%H%M")
startTime = time.time()
logPath = ".\\results\\{0}_{1}_{2}_{3}".format("45C_PD_EDFA2",Vendor,SN,curTime)
os.mkdir(logPath)

### Power meter init
host = "172.29.150.126"
port = 1234
PM_addr = 22
prologix = Prologix(host, port)
PM = HP8152A(PM_addr, prologix)
#PM.write("*RST")
time.sleep(1)
printLog(PM.deviceID)

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
### test cases
#Pcal=11.12 # EDFA input power
Pcal=11.05
#Gain=19
AttList=[]
PinList=[]
PoutList=[]
PDinList=[]
PDoutList=[]
PmeasList=[]
PDinAcc=[]
PDoutAcc=[]

###PD in test
hal.write("hw 1 ofp2 2 x setPeriodActionStatus ALL_ACTION 0")
#hal.write("hw 1 ofp2 3 c x SetEdfaOperatingMode EDFA_1 AGC") 
#hal.write("hw 1 ofp2 3 c x SetEdfaOperatingMode EDFA_2 AGC") 
hal.read_raw()
time.sleep(1)
P0=10
print("Start Testing PD in ...")
for i in range(25):
    
    Att=Pcal+0.579-P0+i*2
    Pin=P0-i*2
#    Pout=Pin+Gain
    #Att=0.58 #for cal only
    AttList.append(Att)
    PinList.append(Pin)
#    PoutList.append(Pout)
    Att_cmd="LINS10:INP:ATT " + str(Att)+ " DB"
    iqs.write(Att_cmd)
    time.sleep(3.5)
    hal.write("hw 1 ofp2 2 c x GetPower PD6")
    data=hal.read_raw().decode()
    data = re.split(r'\r|\n', data)
    PDin=float(data[2])/100 #dBm
    PDinList.append(PDin)
    PDinDelta=PDin-Pin
    PDinAcc.append(PDinDelta)
#    
#    G_cmd="show amplifier-1/1.3/pa"
#    amp=cli.cliSend(G_cmd).decode('utf-8')
#    PDin=re.findall(r"input-power-mon (.+) dBm\r\r\r\n", amp)
#    PDin=float(PDin[0])
#    PDinList.append(PDin)
#    PDinDelta=PDin-Pin
#    PDinAcc.append(PDinDelta)


###PD out test
#hal.write("hw 1 ofp2 2 c x SetEdfaOperatingMode EDFA_1 APC") 
hal.write("hw 1 ofp2 2 c x SetEdfaOperatingMode EDFA_2 APC")
hal.read_raw()
time.sleep(1)     
iqs.write("LINS10:INP:ATT 20 DB")
#cli.write("set amplifier-1/1.3/pa control-mode manual")
print("Start Testing PD out ...")
for i in range(20):
    
    Pout=18-i*2 #dBm
    PoutList.append(Pout)
    Pout_cmd="hw 1 ofp2 2 c x SetPowerSetting EDFA_2 " + str(Pout*100) #mdBm
    hal.write(Pout_cmd)
    hal.read_raw()
    time.sleep(0.5)

    Pmeas=PM.power
    Pmeas=Pmeas+1.85 #calibration offset
    PmeasList.append(Pmeas)
    
    hal.write("hw 1 ofp2 2 c x GetPower PD5")
    data=hal.read_raw().decode()
    data = re.split(r'\r|\n', data)
    PDout=float(data[2])/100 #dBm
    PDoutList.append(PDout)
    #PDoutDelta=PDout-Pout
    PDoutDelta=PDout-Pmeas
    PDoutAcc.append(PDoutDelta)
    time.sleep(0.5)

       
iqs.close()
prologix.close()
#cli.SSH_close()    
hal.SSH_close() 

usl=[]
lsl=[]
usl1=[0.5]*22
usl2=[1]*3
usl=usl1+usl2
lsl1=[-0.5]*22
lsl2=[-1]*3
lsl=lsl1+lsl2
#fig = plt.figure(figsize=(12, 8))
#pdin,=plt.plot(PinList, PDinList)
fig = plt.figure(figsize=(12, 8))
pdinacc,=plt.plot(PinList, PDinAcc, "-o")
usl,=plt.plot(PinList, usl, "r")
lsl,=plt.plot(PinList, lsl, "r")
plt.ylim((-1,1))
plt.xlabel("Input Power [dBm]")
plt.ylabel("PD In Accuracy [dB]")
plt.grid()
plt.savefig(logPath+"\\PD In Accuracy.png", format='png', dpi=96)

usl1=[0.5]*17
usl2=[1]*3
usl=usl1+usl2
lsl1=[-0.5]*17
lsl2=[-1]*3
lsl=lsl1+lsl2
fig = plt.figure(figsize=(12, 8))
pdoutacc,=plt.plot(PoutList, PDoutAcc, "-o")
usl,=plt.plot(PoutList, usl, "r")
lsl,=plt.plot(PoutList, lsl, "r")
plt.ylim((-1,1))
plt.xlabel("Output Power [dBm]")
plt.ylabel("PD Out Accuracy [dB]")
plt.grid()
plt.savefig(logPath+"\\PD Out Accuracy.png", format='png', dpi=96)
 
    ###data saving
curTime = datetime.utcnow().strftime("%Y%m%d%H%M")
f = open(logPath+"\\PD_{0}_{1}_data.log".format(SN,curTime), "w+")
print ("SUMMARY RESULTS:",file=f)
print ("======================",file=f)
#print ("Gain (dB)	{0}".format(Gain),file=f)
#print ("----------------",file=f)
print ("{0}	{1}	{2}".format("Input Power","PDin","PD In Accuracy"), file=f)
for j in range(len(PDinList)):
    print ("{0}	{1}	{2}".format(PinList[j],PDinList[j],PDinAcc[j]), file=f)
print ("----------------",file=f)
#print ("{0}	{1}	{2}	{3}".format("Output Power","Power Meas","PDout","PD Out Accuracy"), file=f)
#for j in range(len(PDoutList)):
#    print ("{0}	{1}	{2}	{3}".format(PoutList[j],PmeasList[j],PDoutList[j],PDoutAcc[j]), file=f)    
#f.close()
print ("{0}	{1}	{2}".format("Output Power","PDout","PD Out Accuracy"), file=f)
for j in range(len(PDoutList)):
    print ("{0}	{1}	{2}".format(PmeasList[j],PDoutList[j],PDoutAcc[j]), file=f)    
f.close()
        

   
costTime = (time.time() - startTime) / 60
printLog("Cost time = {0}mins".format(str(costTime)))
printLog("")

	# change the raw file name with new information
GLB_LOG_FILE.close()
os.rename(".\\results\\tmpLog.log", logPath+"\\printLog.log") 
