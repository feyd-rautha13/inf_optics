# /usr/bin/env python
# -*- coding : utf-8 -*-

'''
Code test
'''

import sys


interface_path = "D:\\work\\coding\\python\\inf_optics\\interface"
component_path = "D:\\work\\coding\\python\\inf_optics\\Test\\component"
labdevice_path = "D:\\work\\coding\\python\\inf_optics\\labdevice"
meas_path = 'D:\\work\\coding\\python\\inf_optics\\Test\\measure'


sys.path.append(interface_path)
sys.path.append(component_path)
sys.path.append(labdevice_path)
sys.path.append(meas_path)

###############################################
from Luna_measure_script import test
import time

################ result path  ####################################
 
path_mux = "C:\\Users\\lab\\Desktop\\rawdata\\NELAWG\\mux\\"  
path_demux = "C:\\Users\\lab\\Desktop\\rawdata\\NELAWG\\demux\\" 

####################################################
luna_ip = '10.13.11.254'
luna_port = 1
groove_ip = '10.13.11.252'





def FullTest(result_path, filename):
    start_time = time.time()
    print("Start Test!")

    print("---------------------------------------")
    
    test(result_path, filename)    
    
    time.sleep(20)   

    stop_time = time.time()
    print("channel {0} test finished!".format(filename))
    print('Total test time is {0}'.format(stop_time-start_time))





