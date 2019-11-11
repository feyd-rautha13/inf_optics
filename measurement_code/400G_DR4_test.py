# /usr/bin/env python
# -*- coding : utf-8 -*-

'''
QSFP-DD DR4 Tx test, all device

'''

#----- Add lib path ------
interface_path = "D:\\work\\coding\\python\\inf_optics\\interface"
component_path = "D:\\work\\coding\\python\\inf_optics\\Test\\component"
device_path = "D:\\work\\coding\\python\\inf_optics\\labdevice"
eeprom_path = "D:\\project\\pluggable\\400G\\400G EEPROM\\QSFP-DD EEPROM Spec-Mar25.xlsx"

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


tm = HP34970A(GPIB_34970, prologix)
tm.set_slot()

gp = GP700(GPIB_Dicon, prologix)
osa = MS9710B(GPIB_ms9710, prologix)
hp1 = AG8164B(GPIB_8164, prologix)
sw = HP86060C(GPIB_HP86060, prologix)
dr4 = QSFPDD(hal,1,7)


###############################################

dut_tx_l1 = 1
dut_tx_l2 = 2
dut_tx_l3 = 3
dut_tx_l4 = 4

dut_rx_L1 = 1
dut_rx_L2 = 2
dut_rx_L3 = 3
dut_rx_L3 = 4

dr4_wavelength = 1311

Tx_IL = [2.26,1.5,1.69,1.79]
Rx_IL = [1.83,1.87, 1.72 ,1.70 ]
ER = 4.734

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
        hal.write("hw 1 vega 1 x setLoopback FACILITY 0 1")
        hal.write("hw 1 vega 2 x setLoopback FACILITY 0 1")
    elif port==9:
        hal.write("hw 1 vega 3 x setLoopback FACILITY 0 1")
        hal.write("hw 1 vega 4 x setLoopback FACILITY 0 1")
    elif port == 10:
        hal.write("hw 1 vega 5 x setLoopback FACILITY 0 1")
        hal.write("hw 1 vega 6 x setLoopback FACILITY 0 1")
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

def GetBER(measuretime=10):
    box.ResetTest()
    time.sleep(measuretime)

    l4 = box.BERperLane(4)
    l5 = box.BERperLane(5)
    return 0.5*(l4+l5)


##################################################################
    
def Power2OMA(power, ER):
    ER = 10**(ER/10)
    OMA = power + 10*np.log10((ER-1)/(ER+1))
    return OMA          


def TxMeasure(lane = 1):
    gp.MSwitchChannel = lane
    sw.MSwitchChannel = lane

    SwitchToPM()
    hp1.pmWav = dr4_wavelength
    time.sleep(3)
    Tx_pwr = hp1.pmPower + Tx_IL[lane - 1]
    Tx_pwr_monitor = dr4.ModMonTxPwr(lane)
    Tx_bias = dr4.ModMonTxBias(lane)
    


    SwitchToOSA()
    
    osa.osaStaWav = dr4_wavelength-6.5
    time.sleep(3)
    osa.osaStoWav = dr4_wavelength+6.5
    
    time.sleep(3)

    osa.osaSingleScan()
    osa.osaPlotTrace(lane)
    spectrum= osa.osaGetPeakWav()

    SwitchToRefRx()
    
    print('-------------------------------------')
    print('Tx bias monitor {:.3}'.format(Tx_bias))
    print('Tx power {:.3}'.format(Tx_pwr))
    print('Tx power monitor {:.3}'.format(Tx_pwr_monitor))
    
    print('Center Wavelength {}'.format(spectrum[0]))
    print('SMSR {}'.format(spectrum[4]))
    
#    return Tx_pwr,Tx_pwr_monitor, Tx_bias, spectrum[0],spectrum[4]



def RxSen(lane = 1, ref_er = 4.734 ,measuretime = 8):
    
    start_time = time.time()
    
    hp1.attValue = 0
    time.sleep(3)
    start_power = np.floor(hp1.attOutPutPower)
    
    rxpwr = []
    rxoma = []
    rxpwr_mon = []
    ber = []
    print('pwr','\t','pwr_mon','\t', 'pwr_oma','\t','BER','\t','Rxlos','\t','Rxlol')

    if start_power<-12:
        print("Error found on Source")
    else:
        stop_power = -20
        
        step_num = 2*(start_power - stop_power) + 1
        
        SwitchToRefRx()
        gp.MSwitchChannel = lane
        sw.MSwitchChannel = lane
        
        attpwr = np.linspace(start_power,stop_power,step_num )       
        time.sleep(20)
   
        for i in attpwr:
            hp1.attOutPutPower = i
            box.ResetTest()
            time.sleep(5)
            los_l4 = box.PatternSync(4)
            los_l5 = box.PatternSync(5)
            Rxlos = dr4.ModMonRxLos(lane)
            Rxlol = dr4.ModMonRxCDRLoL(lane)
            
            if los_l4|los_l5 != 1:
                pwr = i-Rx_IL[lane-1]
                Cuber = GetBER(measuretime)
                pwr_mon = dr4.ModMonRxPwr(lane)
                pwr_oma = Power2OMA(pwr, ref_er)
                
                rxpwr_mon.append(pwr_mon)
                rxpwr.append(pwr)
                rxoma.append(pwr_oma)
                ber.append(Cuber)
                
                print(pwr,'\t',pwr_mon,'\t', pwr_oma,'\t',Cuber,'\t',Rxlos,'\t',Rxlol)
                
            elif Rxlos != 1:
                pwr = i-Rx_IL[lane-1]
                Cuber = 'N/A'
                pwr_oma = 'N/A'
                
                pwr_mon = dr4.ModMonRxPwr(lane)  
                print(pwr,'\t',pwr_mon,'\t', pwr_oma,'\t',Cuber,'\t',Rxlos,'\t',Rxlol)
            else:
                pwr = i-Rx_IL[lane-1]
                Cuber = 'N/A'
                pwr_oma = 'N/A'
                pwr_mon = dr4.ModMonRxPwr(lane)  
                print(pwr,'\t',pwr_mon,'\t', pwr_oma,'\t',Cuber,'\t',Rxlos,'\t',Rxlol)
                pwr_los = i
                break
    print("#######Los D Test########")

    while(True):

        hp1.attOutPutPower = pwr_los
        Rxlos = dr4.ModMonRxLos(lane)
        Rxlol = dr4.ModMonRxCDRLoL(lane)
        pwr1 = pwr_los - Rx_IL[lane-1]
        Cuber = 'N/A'
        pwr_oma = 'N/A'
        pwr_mon = dr4.ModMonRxPwr(lane)
        
        if Rxlos != 0:
            pwr_los += 0.3

            print(pwr1,'\t',pwr_mon,'\t', pwr_oma,'\t',Cuber,'\t',Rxlos,'\t',Rxlol)
        else:
            print(pwr1,'\t',pwr_mon,'\t', pwr_oma,'\t',Cuber,'\t',Rxlos,'\t',Rxlol)
            break
            
            
            
    hp1.attValue = 4       
    stop_time = time.time()
    print('Total time is {0}s'.format(stop_time - start_time))    
#    return rxpwr,rxpwr_mon,rxoma,ber
    

    
        



'''
#1
CHM2T_client_400G(9)

time.sleep(20)

#2
Facility_loopback(9)
    
#3    
dr4.ModInfo()
tm.get_temp(202)
dr4.ModMonCaseTemp
dr4.ModMonInpVcc
hp1.attValue = 0

for i in [1,2,3,4]:
    TxMeasure(i)

for i in [1,2,3,4]:
    print('--------------{0}--------------'.format(i))
    print('--------------{0}--------------'.format(i))
    print('--------------{0}--------------'.format(i))
    RxSen(i)
    

prologix.TCP_close() 
'''   

