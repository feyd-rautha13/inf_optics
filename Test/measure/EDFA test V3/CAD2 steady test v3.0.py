# /usr/bin/env python
# -*- coding : utf-8 -*-

__author__ = 'Youbin Zheng'
__version__ = "3.0" 
# updated gain accuracy algorithm
# added 15ch MAP200 laser source
# added Pol scrambler
# recofig for Tcase test
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
#hal = groove_Hal()

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
logPath = ".\\results\\{0}_{1}_{2}_{3}".format("45C_Steady_EDFA2",Vendor,SN,curTime)
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

iqs.write("LINS13:ROUT:SCAN 2")
iqs.write("LINS14:ROUT:SCAN 2")
iqs.write("LINS17:ROUT:SCAN 1")

iqs.write("LINS10:INP:ATT 10 DB")   
iqs.write("LINS11:ROUT:SCAN 2")
iqs.write("LINS12:ROUT:SCAN 2")
printLog(iqs.read_raw())
time.sleep(20)  #time adjust to activate the IQS

###OSA init
host = "172.29.150.126"
port = 1234
OSA_addr = 8
prologix = Prologix(host, port)
osa = AQ6370(OSA_addr, prologix)
osa.Init
time.sleep(1)
print(osa.data_parse(osa.deviceID))

##########OSA Config#############

#osa.write("AUTO")
#time.sleep(5)
osa.StaWav=1528
osa.StoWav=1568
#osa.MPT=1001

osa.Res=0.1
#osa.write("WNFOFI3.52"); #Pcal=11.12
#osa.write("WNFOFO3.79");
osa.write("WNFOFI3.36"); #Pcal=10.83
osa.write("WNFOFO3.95");

osa.write("SHI1");
#osa.write("SNAT");
osa.write("WDMNOIBW0.1");
osa.write("LSCL10.0");

#osa.write("FIXB")
#osa.write("BLKB")
osa.write("FIXC")
osa.write("BLKC")
#osa.write("DSPA")
#osa.write("SRQ1")


### test cases
#Pcal=11.12 # EDFA input power
Pcal=11.05
AttList=[]
#Pin=[-10, -13, -16, -19, -22, 11.3, 8.3, 5.3, 2.3,-0.7]
#Gain=[10, 13, 16, 19, 22, 10, 13, 16, 19, 22]

Pin=[-12, 8, -16, 4, -20, 0, -26, -6]
Gain=[10, 10, 14, 14, 18, 18, 24, 24]
NFspec=[14.2, 14.2, 9.6, 9.6, 6.4, 6.4, 5.5, 5]

for i in range(8):
#for i in range(len(Pin)):
    print("Start Testing Case #" +str(i)+"...")
    G_cmd="hw 1 ofp2 2 c x SetGainSetting EDFA_2 " + str(Gain[i]*100)

    #G_cmd="set amplifier-1/1.3/pa target-gain " + str(Gain[i]*10)
    hal.write(G_cmd)
    time.sleep(1)
    
        ####Switch to b2b

    iqs.write("LINS11:ROUT:SCAN 2")
    iqs.write("LINS12:ROUT:SCAN 2")
    
    Att=(Pcal-Pin[i])+0.579
    #Att=0.58 #for cal only
    #AttList.append(Att)
    Att_cmd="LINS10:INP:ATT " + str(Att)+ " DB"
    iqs.write(Att_cmd)
    time.sleep(1)
    #iqs.write("LINS10:INP:ATT 5 DB")

    #input("Click Acq. In, then press <Enter>")
    ###Pre-amp spectrum in trace A
    osa.write("ACTV0")
    osa.write("WRTA")
    osa.write("SGL")
    #osa.write("SD1")
    query = int(osa.query("SWEEP?"))
    while query > 0:
        time.sleep(.2)
        query = int(osa.query("SWEEP?"))
    t_active = int(osa.query("ACTV?"))
    trace = "ABC"[t_active]
    
    #osa.write("LDTDIG3")
    #a=osa.Get_X()
    X=osa.query("WDAT"+trace, flag=b"\r\n", endnumber=2).decode('utf8')
    #time.sleep(0.5)
    X=X.rstrip().split(",")[1:]
    X0 = [float(x) for x in X]
    #fig = pl.figure(figsize=(8, 6))
    #pl.plot(i, X, 'o-')
    
    Y=osa.query("LDAT"+trace, flag=b"\r\n", endnumber=2).decode('utf8')
    #time.sleep(0.5)
    Y=Y.rstrip().split(",")[1:]
    Y0 = [float(x) for x in Y]
    #b=osa.query("LDATA")
    #fig = pl.figure(figsize=(8, 6))
    #pl.plot(X0, Y0)
    
    osa.write("FIXA")
    time.sleep(1)
    
#    osa.write("WDMABS")
#    A=osa.query("ANA?").decode('utf8').rstrip().split(",")
#    printLog("Pre-amp Power:" + str(A))
    
    ####Switch to amplifer
    iqs.write("LINS11:ROUT:SCAN 1")
    iqs.write("LINS12:ROUT:SCAN 1")
    time.sleep(1)
    
    #input("Click Acq. Out, then press <Enter>")
    osa.write("ACTV1")
    osa.write("WRTB")
    osa.write("DSPB")
    osa.write("SGL")
    query = int(osa.query("SWEEP?"))
    while query > 0:
        time.sleep(.2)
        query = int(osa.query("SWEEP?"))
    t_active = int(osa.query("ACTV?"))
    trace = "ABC"[t_active]
    trace="B"
    
    X=osa.query("WDAT"+trace, flag=b"\r\n", endnumber=2).decode('utf8')
    #time.sleep(0.5)
    X=X.rstrip().split(",")[1:]
    X1 = [float(x) for x in X]
    #fig = pl.figure(figsize=(8, 6))
    #pl.plot(i, X, 'o-')
    
    Y=osa.query("LDAT"+trace, flag=b"\r\n", endnumber=2).decode('utf8')
    #time.sleep(0.5)
    Y=Y.rstrip().split(",")[1:]
    Y1 = [float(x) for x in Y]
    #b=osa.query("LDATA")
    osa.write("FIXB")
    time.sleep(1)

    
    ###NF analysis
    
    osa.write("WNFAN")
    C=osa.query("ANA?").decode('utf8').rstrip().split(",")
    printLog("EDFA NF:" + str(C))
    

    WL=[]
    G=[]
    GS=[]
    GR=[]
    NF=[]
    j=0
    Pisum=0
    Posum=0
    for j in range(15):
        WLi=float(C[1+j*7])
        WL.append(WLi)
        Gi=float(C[6+j*7])
        G.append(Gi)
        NFi=float(C[7+j*7])
        NF.append(NFi)
        Pi=float(C[2+j*7])
        Pisum=Pisum+10**(Pi/10)
        Po=float(C[3+j*7])
        Posum=Posum+10**(Po/10)
                
    poly = np.polyfit(WL, G, 1)
    p1 = np.poly1d(poly)
    GS = p1(WL)
    #GS = GS.tolist() 
    GR=np.array(G)-GS
    GRpp=max(GR)-min(GR)
    #Tilt=poly[0]*(max(WL)-min(WL))
    Tilt=poly[0]*(1566.93-1528.58)
    
#    GA1=max(G)-Gain[i]
#    GA2=Gain[i]-min(G)
#    GA=max(GA1,GA2)
#    if GA==GA1:
#        Gm=max(G)
#    else:
#        Gm=min(G)
#    GA=Gm-Gain[i]
    
    Gavg=10*math.log10(Posum/Pisum)
    GA=Gavg-Gain[i]
    
    GF=max(G)-min(G)
    NFm=max(NF)
 
    ###data saving
    fig = plt.figure(figsize=(12, 8))
    pre,=plt.plot(X0, Y0)
    post,=plt.plot(X0, Y1, "r")
    plt.xlabel("Wavelength [nm]")
    plt.ylabel("Power Level [dBm]")
    plt.ylim((-100,10))
    plt.grid()
    plt.legend([pre, post], ["Pre-amp", "Post-amp"])
    plt.title("Optical Spectrum: Gain="+str(Gain[i])+"dB, "+"Pin="+str(Pin[i])+"dBm")
    plt.savefig(logPath+"\\G{0}_P{1}_spectrum.png".format(Gain[i],Pin[i]), format='png', dpi=96)

    fig = plt.figure(figsize=(12, 8))
    ax1 = fig.add_subplot(111)
    Gplt,=ax1.plot(WL, G, "-o")
    GSplt,=ax1.plot(WL, GS, "--")
    GRplt,=ax1.plot(WL, GR, "-ro")
    #plt.ylim((-1,1))
    ax1.set_xlabel("Wavelength [nm]")
    ax1.set_ylabel("Gain [dB]")
    ax1.legend([Gplt, GSplt, GRplt], ["Gain", "Gain Slope", "Gain Ripple"],loc="center left")
    #ax1.legend(loc='upper left')
    plt.grid()
    ax2 = ax1.twinx()  
    ax2.plot(WL, NF, '-d',label="NF") 
    ax2.set_ylabel('NF [dB]') 
    ax2.set_ylim((0,20))
    #ax2.legend("NF",loc='center right')
    ax2.legend(loc="center right")
    plt.title("Steady State: Gain="+str(Gain[i])+"dB, "+"Pin="+str(Pin[i])+"dBm")
    plt.savefig(logPath+"\\G{0}_P{1}_{2}.png".format(Gain[i],Pin[i],Tilt), format='png', dpi=96)
    
    curTime = datetime.utcnow().strftime("%Y%m%d%H%M")
    f = open(logPath+"\\G{0}_P{1}_{2}_data.log".format(Gain[i],Pin[i],curTime), "w+")
    print ("SUMMARY RESULTS:",file=f)
    print ("======================",file=f)
    print ("Gain (dB)	{0}".format(Gain[i]),file=f)
    print ("Input Power (dBm)	{0}".format(Pin[i]),file=f)
    print ("----------------",file=f)
#    print ("Max/Min Gain (dB)	{0}".format(Gm),file=f)
    print ("Gain Accuracy (dB)	{0}	{1}".format(GA,"+/-0.5dB"),file=f)
    print ("Gain Tilt (dB)	{0}	{1}".format(Tilt,"+/-0.5dB"),file=f)
    print ("Gain Ripple (dB)	{0}	{1}".format(GRpp,"<1.2dB"),file=f)
    print ("Gain Flatness (dB)	{0}	{1}".format(GF,"<1.5dB"),file=f)
    print ("Noise Figure (dB)	{0}	{1}".format(NFm,"<"+str(NFspec[i])+"dB"),file=f)
    print ("----------------",file=f)
    print ("{0}	{1}	{2}".format("Wavelength","Gain","NF"), file=f)
    for j in range(14):
    	print ("{0}	{1}	{2}".format(WL[j],G[j],NF[j]), file=f)
    f.close()
    
    f = open(logPath+"\\Summary_steady_data.log", "a+")
    print ("SUMMARY RESULTS:",file=f)  
    print ("======================",file=f)
    print ("Gain (dB)	{0}".format(Gain[i]),file=f)
    print ("Input Power (dBm)	{0}".format(Pin[i]),file=f)
    print ("----------------",file=f)
#    print ("Max/Min Gain (dB)	{0}".format(Gm),file=f)
    print ("Gain Accuracy (dB)	{0}	{1}".format(GA,"+/-0.5dB"),file=f)
    print ("Gain Tilt (dB)	{0}	{1}".format(Tilt,"+/-0.5dB"),file=f)
    print ("Gain Ripple (dB)	{0}	{1}".format(GRpp,"<1.2dB"),file=f)
    print ("Gain Flatness (dB)	{0}	{1}".format(GF,"<1.5dB"),file=f)
    print ("Noise Figure (dB)	{0}	{1}".format(NFm,"<"+str(NFspec[i])+"dB"),file=f)
    f.close()
   

iqs.close()
hal.SSH_close()

f = open(logPath+"\\Summary_steady_data.log", "a+")
print ("",file=f)
print ("======================",file=f)
print ("EDFA	#2 Add",file=f) 
print ("SN	{0}".format(str(SN)),file=f)  
print ("Vendor	{0}".format(str(Vendor)),file=f)
print ("FW Rev	{0}".format(str(FW)),file=f)  
print ("HW Rev	{0}".format(str(HW)),file=f)
f.close()
   
costTime = (time.time() - startTime) / 60
printLog("Cost time = {0}mins".format(str(costTime)))
printLog("FW Rev = {0}".format(str(FW)))
printLog("HW Rev = {0}".format(str(HW)))
printLog("")

	# change the raw file name with new information
GLB_LOG_FILE.close()
os.rename(".\\results\\tmpLog.log", logPath+"\\printLog.log") 
