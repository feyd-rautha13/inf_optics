# /usr/bin/env python
# -*- coding : utf-8 -*-

'''
QSFP-DD DR4 Tx test, all device

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
#from transceiver import QSFPDD
from transceiver import QSFP28


# ------ import 3rd part lib ------------


# -- declare vars ----------------
#groove_ip = '172.29.150.194'
#groove_ip = '10.13.15.114'
groove_ip_su = '172.29.201.124'


# ------ class instance ------
#hal = groove_Hal(host = groove_ip,port = 8022, 
#                 username = 'administrator' , password = 'e2e!Net4u#',
#                 timeout = 10, halusername = 'su', halpassword = 'cosh1$')
hal = groove_Hal(host = groove_ip_su,port = 8022, 
                 username = 'administrator' , password = 'e2e!Net4u#',
                 timeout = 10, halusername = 'su', halpassword = 'cosh1$')



#qdd1 = QSFPDD(hal,1,6)
#qdd2 = QSFPDD(hal,1,7)
#qdd3 = QSFPDD(hal,1,8)

q28 = QSFP28(hal,4,1,1)



# -- define temp test function --

    


#####################################################



