# /usr/bin/env python
# -*- coding : utf-8 -*-


# ---------- Test script template -----------------



#----- Add lib path ------
path1 = "D:\\work\\coding\\python\\inf_optics\\interface"
path2 = "D:\\work\\coding\\python\\inf_optics\\Test\\component"
path3 = "D:\\work\\coding\\python\\inf_optics\\labdevice"

#---------------
import sys
sys.path.append(path1)
sys.path.append(path2)
sys.path.append(path3)


#----- import user defined lib --------
from SSHinterface import groove_Hal
from transceiver import QSFPDD
from EXFO_LTB8 import LTB8

# ------ import common lib ------------
import numpy as np
import openpyxl
import threading
import time
from datetime import datetime


# -- declare vars ----------------
groove_ip = '172.29.150.194'
LTB_ip = "172.29.150.191"
LTB_port = 5025

# ------ class instance ------


box = LTB8(LTB_ip, LTB_port)
fr4 = QSFPDD(hal,1,8)



# ------- define temp function --------------------


def temp_function(argv):
    pass

# ---------- Test Main function -----------

if __name__ == "__main__":
    temp_function(argv)

        
    
    
    
    
    
    
    
    
    
