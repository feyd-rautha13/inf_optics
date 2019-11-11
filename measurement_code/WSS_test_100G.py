# /usr/bin/env python
# -*- coding : utf-8 -*-

'''
Code test
'''

import sys
#channel_plan_path = 'D:\\work\\coding\\python\\OpticalTest\\code\\wss_channelplan_100G.csv'
channel_plan_path = 'D:\\work\\coding\\python\\OpticalTest\\code\\wss_channelplan_50G.csv'

interface_path = "D:\\work\\coding\\python\\inf_optics\\interface"
component_path = "D:\\work\\coding\\python\\inf_optics\\Test\\component"
labdevice_path = "D:\\work\\coding\\python\\inf_optics\\labdevice"
meas_path = 'D:\\work\\coding\\python\\inf_optics\\Test\\measure'


sys.path.append(interface_path)
sys.path.append(component_path)
sys.path.append(channel_plan_path)
sys.path.append(labdevice_path)
sys.path.append(meas_path)

###############################################
from SSHinterface import groove_Hal
from OFP2 import O2O1x4WSS
from ova5000 import Luna
from Luna_measure_script import test
import numpy as np
import time

################ result path  ####################################
 
result_path_p1 = "C:\\Users\\lab\\Desktop\\rawdata\\WSSP1\\9H1370432\\50G\\port1\\"  
result_path_p2 = "C:\\Users\\lab\\Desktop\\rawdata\\WSSP1\\9H1370432\\50G\\port2\\"
result_path_p3 = "C:\\Users\\lab\\Desktop\\rawdata\\WSSP1\\9H1370432\\50G\\port3\\"
result_path_p4 = "C:\\Users\\lab\\Desktop\\rawdata\\WSSP1\\9H1370432\\50G\\port4\\"

####################################################
luna_ip = '10.13.11.254'
luna_port = 1
groove_ip = '10.13.11.252'


hal = groove_Hal(host = groove_ip,port = 8022, 
                 username = 'administrator' , password = 'e2e!Net4u#',
                 timeout = 10, halusername = 'su', halpassword = 'cosh1$')


wss = O2O1x4WSS(hal, card = 1, subslot=3)

#setp 1 
#channel setting
channel_plan = np.loadtxt(channel_plan_path, delimiter = ',', usecols=(0,1))

chn_id = channel_plan[0:,0]
chn_id = [int(x) for x in chn_id]
chn_freq = channel_plan[0:,1]

###############--Set Channel ID--############################
#Open/Even/Odd chn_id Generation

Open_chnId = [x for x in chn_id if x!=0]
Even_chnId=[x for x in chn_id if np.mod(x,2)==1]
Odd_chnId=[x for x in chn_id if (np.mod(x,2)==0 and x!=0) ]


################--Set Port ID --#############################
p1 = 0
p2 = 1
p3 = 2
p4 = 3
############################################################

    
def ResetAllChn():
    for i in Open_chnId:
        wss.Blocking(chn_id[i])
        time.sleep(0.2)
    for i in Open_chnId:
        wss.SetChnAtt(chn_id[i],0)
        time.sleep(0.5)
def ConChnPlan(bandwidth=50):
    for i in Open_chnId:
        wss.ConfigChn(chn_id[i], chn_freq[i],int(bandwidth))
        time.sleep(0.5)

def DelChnPlan():
    for i in Open_chnId:
        wss.DelChn(chn_id[i])




def FullTest(port=p1, result_path=result_path_p1):
    start_time = time.time()
    print("Start Test!")
    print("Port {0} test Started!".format(port+1))
    print("---------------------------------------")
    
    ########---Reset All Channels---##########
    ResetAllChn()


    #################### -- Route EVEN 100 0dB -- ###########################    
    for i in Even_chnId:
        wss.Routing(chn_id[i], port)
        time.sleep(0.2)    
    
    
    #################### -- Test EVEN 100 0dB -- ###########################   
    test(result_path,"EVEN_100_0dB")    
    time.sleep(20)   
    
    
    #################### -- EVEN 100G 5dB -- ###########################    
    for i in Even_chnId:
        wss.SetChnAtt(chn_id[i], 5)
        time.sleep(0.2)      
    
    test(result_path,"EVEN_100G_5dB")     
    time.sleep(20)
    
    #################### -- EVEN 100G 10dB -- ###########################    
    for i in Even_chnId:
        wss.SetChnAtt(chn_id[i], 10)
        time.sleep(0.2)    
     
    test(result_path,"EVEN_100G_10dB") 
    time.sleep(20)
    
    #################### -- EVEN 100G 15dB -- ###########################    
    for i in Even_chnId:
        wss.SetChnAtt(chn_id[i], 15)
        time.sleep(0.2)    
     
    test(result_path,"EVEN_100G_15dB") 
    time.sleep(20)
        
    ########---Reset All Channels---##########
    ResetAllChn()
       
        
        
    #################### -- Route Odd 100G 0dB -- ###########################    
    for i in Odd_chnId:
        wss.Routing(chn_id[i], port)
        time.sleep(0.2)  
    
    #################### -- Test Odd 100G 0dB -- ###########################  
    test(result_path,"ODD_100G_0dB")       
    time.sleep(20)   
       
    #################### -- Odd 100G 5dB -- ###########################    
    for i in Odd_chnId:
        wss.SetChnAtt(chn_id[i], 5)
        time.sleep(0.2)  
    
    
    test(result_path,"ODD_100G_5dB")      
    time.sleep(20)
        
    #################### -- Odd 100G 10dB -- ###########################    
    for i in Odd_chnId:
        wss.SetChnAtt(chn_id[i], 10)
        time.sleep(0.2)  
    
    test(result_path,"ODD_100G_10dB")     
    time.sleep(20)
    
    #################### -- Odd 100G 15dB -- ###########################    
    for i in Odd_chnId:
        wss.SetChnAtt(chn_id[i], 15)
        time.sleep(0.2)  
    
    
    test(result_path,"ODD_100G_15dB") 
    time.sleep(20)
    
    ########---Reset All Channels---##########
    ResetAllChn()
    ##########################################  
    
    #################### -- Open 100G 0dB -- ###########################      
    for i in Open_chnId:
        wss.Routing(chn_id[i],p1)
        time.sleep(0.2)
        
    test(result_path,"Open_100G_0dB") 
    time.sleep(20)
    ####################################################################

    ########---Reset All Channels---##########
    ResetAllChn()
    ########################################## 
    stop_time = time.time()
    print("Port {0} test finished!".format(port))
    print('Total test time is {0}'.format(stop_time-start_time))



'''
# Config channel plan
ConChnPlan(50)

############ p1 #####################
FullTest(p1, result_path_p1)

############ p2 #####################
FullTest(p2, result_path_p2)

############ p3 #####################
FullTest(p3, result_path_p3)

############ p3 #####################
FullTest(p4, result_path_p4)
'''

