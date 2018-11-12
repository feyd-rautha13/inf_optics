from luna import *
from TCPinterface import *




luna.query("*STB?")


luna.write("*POC 1")#0, disable event status register; 1, enable event status register
luna.query("*POC?") #0, the former command is not completed; 1, the former command is completed

luna.write("QUIT") #disconnect remote control

###System level commands
luna.query("SYSTem:WARM?")
luna.query("*SYST:WTIM??")
luna.query("SYST:CAL?") #query calibration status, 1:in calibraton; 0: out of calibration
luna.query("SYST:ERR?") #0: indicate the last command complted; if not 0, means we could get a error message by using "SYST:ERRD?"
luna.query("SYST:ERRD?")
luna.query("SYST:LASE?")#1: laser on; 0:laser off
luna.query("SYST:RDY?")#1: ready to scan; 0: not ready
luna.query("SYST:LAST?") #Query the last command
luna.query("SYST:VER?") #query the software version
luna.write("SYST:LOAD") #load .bin file


##configuration commands
luna.write("CONF:CWL 1560.0")
luna.query("CONF:CWL?")

luna.write("CONF:STAR 1555.0")
luna.query("CONF:STAR?")
luna.query("CONF:END?")

luna.write("CONF:RANG 40")
luna.query("CONF:RANG?")

           
##Data capture and retrieval commands
luna.query("FETC:FREQ?")
'''
196585.218164,0.159580\x00', means the start FREQ is 196595.218164 and
frequency increment size/Sample Spacing is 0.159580 GHz.
'''
luna.query("CONF:END?")

luna.query("CONF:RANG?")

luna.query("FETC:TINC?")#This query returns a message in the form “0.000567” ns.

luna.query("FETC:FSIZ?") #return a message about the size data points

luna.write("CONF:TEST 1,1") #  sets the Type of Measurement for full calibration to transmission.
luna.query("CONF:TEST? ")# 0 reflection; 1 transmission

luna.query("FETC:MDET?") #return current measurement information. Full!

#VOA only commands
luna.write("SYST:FCAL") #Full calibration
luna.query("*OPC?") #see whether calibration completed or not

luna.write("SYST:ICAL") #Take a internal calibration
luna.write("SYST:FILT")# Applies the smoothing filter



# File saved ????

luna.write("SYST:SAVS 'D:\\measData.txt'") #Save file to the remote computer. C:/ need portity
luna.query("SYST:ERR?")
luna.query("SYST:ERRD?")

#set-up before scan
luna.write("CONF:AAF 1") #Always use filter
luna.write("CONFigure:AVeraGE 1")#Eanble averaging
luna.write("CONFigure:AVeraGeSet 10,0")#10 times average for measurement
luna.write("CONF:TDW 1")#Apply time domain window
luna.write("CONF:FDUT 1")#Find DUT length automatically
luna.write("CONF:DUTM 1")#1. set the dut length find method to broadband
luna.write("CONF:DUTN 'Red'")#Set the DUT name
luna.query("CONF:DUTN?") #



luna.write("CONF:PDEC 1530,1532")
luna.query("FETC:MEAS? 5")

#calibration
luna.write("CONFigure:AVeraGeSet 20,1")#20 times average for full calibration

#Filter
luna.write("CONF:RSBU 1") #1: Resolution bandwidth units: picometers
luna.query("CONF:RSBU?")#1:Picometers; 0: GHz

luna.write("CONF:FRBW 0.15")#Set Filter Resolution

luna.query("CONF:FRBW?")#Rerutn OVA current filter resolution
luna.query("CONF:TWRB?")#return OVA current Time Domain Window Resolutoin Bandwidth
luna.query("CONF:CRBW?")#return OVA current Convolved Resolution Bandwidth
luna.query("CONF:SRES?")#return OVA current Sample resolution

luna.write("TSIG 0.5")
luna.query("CONF:TSIG?")#return OVA sigma

luna.write("CONF:TLIM 3.0,3.25")
luna.query("CONF:TLIM?")#return the TimeDomain WIndow in Unit 'ns'


luna.write("CONF:TRET 1") #remain setting for Time Domain Window
luna.query("CONF:TRET?") #return setting for TIme Domain WIndow, 1:Remain

luna.write("CONF:THAN 1")#Enable Hanning Window

##OVA-only Data Capture and Retrieval Commands
luna.query("FETC:JONE?")
luna.query("FETC:XAXI?  0")

'''
The parameter x can take values from 0 to 4:
0 - Frequency Domain (nm)
1 - Frequency Domain (GHz)
2 - Frequency Domain (THz)
3 - Time Domain (ns)
4 - Frequency Domain (m)
'''








