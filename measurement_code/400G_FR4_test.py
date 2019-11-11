# /usr/bin/env python
# -*- coding : utf-8 -*-

'''
QSFP-DD FR4 Tx test, all device

'''

#----- Add lib path ------
interface_path = "D:\\work\\coding\\python\\inf_bitbucket\\infinera_instrument_drivers\\interface"
component_path = "D:\\work\\coding\\python\\inf_bitbucket\\infinera_instrument_drivers\\Test\\component"
device_path = "D:\\work\\coding\\python\\inf_bitbucket\\infinera_instrument_drivers\\labdevice"


import sys
sys.path.append(interface_path)
sys.path.append(component_path)
sys.path.append(device_path)


#----- import user defined lib --------
from SSHinterface import groove_Hal
from SSHinterface import groove_cli
from prologix import Prologix
from transceiver import QSFPDD
from hp34970A import HP34970A
from ms9710b import MS9710B
from ag8164b import AG8164B
from gp700 import GP700
from hp86060c import HP86060C
from EXFO_LTB8 import LTB8



# ------ import 3rd part lib ------------
import numpy as np
import time

# -- declare vars ----------------
groove_ip = '172.29.150.194'
prologix_ip = '172.29.150.127'
LTB_ip = "172.29.150.191"

prologix_port = 1234
LTB_port = 5025

GPIB_8164 = 5 
GPIB_34970 = 9
GPIB_ms9710 = 8
GPIB_Dicon = 30
GPIB_HP86060 = 19

# ------ class instance ------
hal = groove_Hal(host = groove_ip,port = 8022, 
                 username = 'administrator' , password = 'e2e!Net4u#',
                 timeout = 10, halusername = 'su', halpassword = 'cosh1$')

cli = groove_cli(host = groove_ip, port = 8022, username = 'administrator', 
                 password = 'e2e!Net4u#')

prologix = Prologix(prologix_ip, prologix_port)

box = LTB8(LTB_ip, LTB_port)
box.ModOperLaneMode()


tm = HP34970A(GPIB_34970, prologix)
tm.set_slot()

gp = GP700(GPIB_Dicon, prologix)
osa = MS9710B(GPIB_ms9710, prologix)
hp1 = AG8164B(GPIB_8164, prologix)
sw = HP86060C(GPIB_HP86060, prologix)
dr4 = QSFPDD(hal,1,7)


###############################################

fr4_wavelength = [0,1271,1291,1311,1331]

Tx_IL = [0,1.5986205,1.52867,1.501441,1.494256]
Rx_IL = [0,1.563,1.532678,1.423598,1.446502]
ER = [0,4.624,4.687,4.734,4.512]

##################################################
def CHM2T_client_400G(port = 10):
    '''
    port 8/9/10 support 400G Mode
    '''
    cli.clear_buffer()
    cli.cli_disable_interactive_mode()
    cli.write("set port-1/1/[3..14] port-mode not-applicable")
    cli.write("set port-1/1/{0}  port-mode 400GBE".format(port))
    cli.write("set port-1/1/{0}  admin-status up".format(port))
    
    
def Facility_loopback(port = 10) :   
    if port==8:
        hal.write("hw 1 vega 1 x setLoopback 2 0 1")
        hal.write("hw 1 vega 2 x setLoopback 2 0 1")
    elif port==9:
        hal.write("hw 1 vega 3 x setLoopback 2 0 1")
        hal.write("hw 1 vega 4 x setLoopback 2 0 1")
    elif port == 10:
        hal.write("hw 1 vega 5 x setLoopback 2 0 1")
#        hal.write("hw 1 vega 6 x setLoopback FACILITY 0 1")
        hal.write("hw 1 vega 6 x setLoopback 2 0 1")
    else:
        print("Wrong port configuration!")

#############################################################
    
def SwitchToOSA():
    gp.SSwitchOut2(1,1)
    gp.SSwitchOut1(2,1)

def SwitchToPM():
    gp.SSwitchOut2(1,1)
    gp.SSwitchOut2(2,1)
    
def SwitchToRefRx():
    gp.SSwitchOut1(1,1)

def GetBER(lane=4, measuretime=10):
    box.ResetTest()
    time.sleep(measuretime)

    l4 = box.BERperLane(2*lane-2)
    l5 = box.BERperLane(2*lane-1)
    return 0.5*(l4+l5)


##################################################################
    
def Power2OMA(power, ER):
    ER = 10**(ER/10)
    OMA = power + 10*np.log10((ER-1)/(ER+1))
    return OMA          


def TxMeasure(lane = 1):
    print("------------L{0} test started---------------".format(lane))
    start_time = time.time()
    hp1.attValue = 0
    
    print("Operate traffic box")
    box.ModOperLaneMode()
    box.ModuleLaserONPerLane(0)
    box.ModuleLaserONPerLane(1)
    box.ModuleLaserONPerLane(2)
    box.ModuleLaserONPerLane(3)

    print("operate traffic route")    
    gp.MSwitchChannel = 5
    sw.MSwitchChannel = 5
    
    print("Select lane under test")
    dr4.ModDisableAllLaser
    dr4.ModEnSingleLane(lane)
    time.sleep(2)
    
    print("Power measurment")
    SwitchToPM()
    hp1.pmWav = fr4_wavelength[lane]
    time.sleep(3)



    Tx_pwr = hp1.pmPower + Tx_IL[lane]
    Tx_pwr_monitor = dr4.ModMonTxPwr(lane)
    Tx_bias = dr4.ModMonTxBias(lane)
    
    print("Specturm measurment")
    SwitchToOSA()
    osa.osaStaWav = 1260
    time.sleep(2)
    osa.osaStoWav = 1340
    time.sleep(2)
    osa.osaStaWav = fr4_wavelength[lane]-6.5
    time.sleep(2)
    osa.osaStoWav = fr4_wavelength[lane]+6.5
    time.sleep(2)

    osa.osaSingleScan()
    osa.osaPlotTrace(lane)
    spectrum= osa.osaGetPeakWav()

    SwitchToRefRx()
    
    print('------------ Result show ----------------')
    print('Tx bias monitor {:.3}'.format(Tx_bias))
    print('Tx power {:.3}'.format(Tx_pwr))
    print('Tx power monitor {:.3}'.format(Tx_pwr_monitor))
    
    print('Center Wavelength {}'.format(spectrum[0]))
    print('SMSR {}'.format(spectrum[4]))
    
    stop_time = time.time()
    print('Total time is {0}s'.format(stop_time - start_time))      
    print("------------L{0} test finished--------------".format(lane))    
#    return Tx_pwr,Tx_pwr_monitor, Tx_bias, spectrum[0],spectrum[4]



def RxSen(lane = 1, ref_er = 4.734 ,measuretime = 8):
    print("---------L{0} test started---------------".format(lane))
    start_time = time.time()
    
    print("Crear traffic loopback route")
    SwitchToRefRx()
    gp.MSwitchChannel = 5
    sw.MSwitchChannel = 5
    
    print("Turn all the Source lanes off")
    box.ModOperLaneMode()
    box.ModuleLaserOFFPerLane(0)
    box.ModuleLaserOFFPerLane(1)
    box.ModuleLaserOFFPerLane(2)
    box.ModuleLaserOFFPerLane(3)
    
    print("Turn all the DUT lanes ON")
    dr4.ModEnableAllLaser
    
    print("Turn Source single lane On")
    box.ModuleLaserONPerLane(lane-1)
    
    print("Set VOA wavelength")
    hp1.attWav = fr4_wavelength[lane]
    time.sleep(3)
    
    print("Initial VOA output power")
    hp1.attOutPutPower = -3
    time.sleep(1)
    
    print("Set VOA attenution to 0dB")
    hp1.attValue = 0
    box.ResetTest()
    time.sleep(3)
    start_power = np.floor(hp1.attOutPutPower)
    hp1.attOutPutPower = start_power
    init_att = hp1.attValue
    
    print("Initial power is {}".format(start_power))
    print("Initial att is {}".format(init_att))
    
    rxpwr = []
    rxoma = []
    rxpwr_mon = []
    ber = []
    pwr_los = 0
    
    print("Turn On all of the Source again")
    box.ModuleLaserONPerLane(0)
    box.ModuleLaserONPerLane(1)
    box.ModuleLaserONPerLane(2)
    box.ModuleLaserONPerLane(3)    
    
    box.ResetTest()
    print("---------------------Test start------------------------")
    time.sleep(3)
    print('pwr','\t','pwr_mon','\t', 'pwr_oma','\t','BER','\t','Rxlos','\t','Rxlol')

    if start_power<-12:
        print("Error found on Source")
    else:
        attpwr = np.linspace(init_att,20+init_att,41)       
        time.sleep(1)
   
        for i in attpwr:
            hp1.attValue = i
            box.ResetTest()
#            time.sleep(15)
            los_l4 = box.PatternSync(lane*2-1)
            los_l5 = box.PatternSync(lane*2-2)
            Rxlos = dr4.ModMonRxLos(lane)
            Rxlol = dr4.ModMonRxCDRLoL(lane)
            
            if los_l4|los_l5 != 1:
                pwr = start_power -(i - init_att) - Rx_IL[lane]
                Cuber = GetBER(lane,measuretime)
                pwr_mon = dr4.ModMonRxPwr(lane)
                pwr_oma = Power2OMA(pwr, ref_er)
                
                rxpwr_mon.append(pwr_mon)
                rxpwr.append(pwr)
                rxoma.append(pwr_oma)
                ber.append(Cuber)
                
                print(pwr,'\t',pwr_mon,'\t', pwr_oma,'\t',Cuber,'\t',Rxlos,'\t',Rxlol)
                
            elif Rxlos != 1:
                pwr = start_power -(i - init_att) - Rx_IL[lane]
                Cuber = 'N/A'
                pwr_oma = 'N/A'
                
                pwr_mon = dr4.ModMonRxPwr(lane)  
                print(pwr,'\t',pwr_mon,'\t', pwr_oma,'\t',Cuber,'\t',Rxlos,'\t',Rxlol)
            else:
                pwr = start_power -(i - init_att) - Rx_IL[lane]
                Cuber = 'N/A'
                pwr_oma = 'N/A'
                pwr_mon = dr4.ModMonRxPwr(lane)  
                print(pwr,'\t',pwr_mon,'\t', pwr_oma,'\t',Cuber,'\t',Rxlos,'\t',Rxlol)
                pwr_los = i
                break
    print("#######Los D Test########")

    while(True):

        hp1.attValue = pwr_los
        Rxlos = dr4.ModMonRxLos(lane)
        Rxlol = dr4.ModMonRxCDRLoL(lane)
        pwr1 = start_power -(pwr_los - init_att) - Rx_IL[lane]
        Cuber = 'N/A'
        pwr_oma = 'N/A'
        pwr_mon = dr4.ModMonRxPwr(lane)
        
        if Rxlos != 0:
            pwr_los -= 0.3

            print(pwr1,'\t',pwr_mon,'\t', pwr_oma,'\t',Cuber,'\t',Rxlos,'\t',Rxlol)
        else:
            print(pwr1,'\t',pwr_mon,'\t', pwr_oma,'\t',Cuber,'\t',Rxlos,'\t',Rxlol)
            break
            
            
            
    hp1.attValue = 3       
    stop_time = time.time()
    print('Total time is {0}s'.format(stop_time - start_time))   
    print("---------L{0} test finished--------------".format(lane))
#    return rxpwr,rxpwr_mon,rxoma,ber
    

    
        



'''
#0
dr4 = QSFPDD(hal,1,7)

#1
CHM2T_client_400G(9)

#2
Facility_loopback(9)
    
#3
SwitchToRefRx()
hp1.attValue = 0
box.ResetTest()

#4    
dr4.ModInfo()
tm.get_temp(202)
dr4.ModMonCaseTemp
dr4.ModMonInpVcc

#5
cls

for i in [1,2,3,4]:
    TxMeasure(i)
    print("\n")
    print("\n")
    print("\n")


cls

for i in [1,2,3,4]:
    RxSen(i, ER[i], 8)
    print("\n")
    print("\n")
    print("\n")

#6
prologix.TCP_close() 
cli.close_session()
box.close()
hal.close_session()


hw 1 vega 1 x setLoopback 2 0 1
hw 1 vega 2 x setLoopback 2 0 1
''' 

