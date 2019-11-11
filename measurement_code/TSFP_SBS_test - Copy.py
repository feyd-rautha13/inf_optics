# /usr/bin/env python
# -*- coding : utf-8 -*-

'''
TSFP+ SBS test, all device

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

from prologix import Prologix
from ag8164b import AG8164B


# ------ import 3rd part lib ------------
import numpy as np
import time

# -- declare vars ----------------

prologix_ip = '172.29.150.127'
prologix_port = 1234
GPIB_8164 = 5 

# ------ class instance ------
prologix = Prologix(prologix_ip, prologix_port)
hp = AG8164B(GPIB_8164, prologix)

######################################################

def test():
    hp.attValue = 0
    time.sleep(3)
    startpower = 0
    stoppower = np.floor(hp.attOutPutPower)
    step_number = 2*(stoppower - startpower)+1
   
    outpowerarray = np.linspace(startpower, stoppower, step_number)
    
    for i in outpowerarray:
        hp.attOutPutPower = i
        time.sleep(2)
        j = hp.pmPower
        time.sleep(1)
        
        print(i,'\t',j,'\t',i-j)
        


   
    
