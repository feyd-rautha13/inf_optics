# /usr/bin/env python
# -*- coding : utf-8 -*-

"""
Created on Tue Apr 02 11:01:44 2019
Modified on 
File description: WSS data analyses 
    
"""

__author__ = 'Sizhan Liu'
__version__ = "1.0"

import sys
import os
import numpy as np
import time
import pylab as pl

#add component class
component_path = "D:\\work\\coding\\python\\inf_optics\\Test\\component\\"

#50G add channel plan
channel_plan_path = "D:\\work\\coding\\python\\OpticalTest\\code\\wss_channelplan_100G.csv "

#add port1 data path
p1_even_trace_0dB = "D:\\project\\OFP2\\2018-04-27 WSS\\2019-06-19 data\\9H1370432\\f_100G\\port1\\f_EVEN_100G_0dB.txt"
p1_odd_trace_0dB = "D:\\project\\OFP2\\2018-04-27 WSS\\2019-06-19 data\\9H1370432\\f_100G\\port1\\f_ODD_100G_0dB.txt"

p1_even_trace_5dB = "D:\\project\\OFP2\\2018-04-27 WSS\\2019-06-19 data\\9H1370432\\f_100G\\port1\\f_EVEN_100G_5dB.txt"
p1_odd_trace_5dB = "D:\\project\\OFP2\\2018-04-27 WSS\\2019-06-19 data\\9H1370432\\f_100G\\port1\\f_ODD_100G_5dB.txt"

p1_even_trace_10dB = "D:\\project\\OFP2\\2018-04-27 WSS\\2019-06-19 data\\9H1370432\\f_100G\\port1\\f_EVEN_100G_10dB.txt"
p1_odd_trace_10dB = "D:\\project\\OFP2\\2018-04-27 WSS\\2019-06-19 data\\9H1370432\\f_100G\\port1\\f_ODD_100G_10dB.txt"

p1_even_trace_15dB = "D:\\project\\OFP2\\2018-04-27 WSS\\2019-06-19 data\\9H1370432\\f_100G\\port1\\f_EVEN_100G_15dB.txt"
p1_odd_trace_15dB = "D:\\project\\OFP2\\2018-04-27 WSS\\2019-06-19 data\\9H1370432\\f_100G\\port1\\f_ODD_100G_15dB.txt"

#add port2 data path
p2_even_trace_0dB = "D:\\project\\OFP2\\2018-04-27 WSS\\2019-06-19 data\\9H1370432\\f_100G\\port2\\f_EVEN_100G_0dB.txt"
p2_odd_trace_0dB = "D:\\project\\OFP2\\2018-04-27 WSS\\2019-06-19 data\\9H1370432\\f_100G\\port2\\f_ODD_100G_0dB.txt"

p2_even_trace_5dB = "D:\\project\\OFP2\\2018-04-27 WSS\\2019-06-19 data\\9H1370432\\f_100G\\Port2\\f_EVEN_100G_5dB.txt"
p2_odd_trace_5dB = "D:\\project\\OFP2\\2018-04-27 WSS\\2019-06-19 data\\9H1370432\\f_100G\\Port2\\f_ODD_100G_5dB.txt"

p2_even_trace_10dB = "D:\\project\\OFP2\\2018-04-27 WSS\\2019-06-19 data\\9H1370432\\f_100G\\Port2\\f_EVEN_100G_10dB.txt"
p2_odd_trace_10dB = "D:\\project\\OFP2\\2018-04-27 WSS\\2019-06-19 data\\9H1370432\\f_100G\\Port2\\f_ODD_100G_10dB.txt"

p2_even_trace_15dB = "D:\\project\\OFP2\\2018-04-27 WSS\\2019-06-19 data\\9H1370432\\f_100G\\Port2\\f_EVEN_100G_15dB.txt"
p2_odd_trace_15dB = "D:\\project\\OFP2\\2018-04-27 WSS\\2019-06-19 data\\9H1370432\\f_100G\\Port2\\f_ODD_100G_15dB.txt"

#add port3 data path
p3_even_trace_0dB = "D:\\project\\OFP2\\2018-04-27 WSS\\2019-06-19 data\\9H1370432\\f_100G\\port3\\f_EVEN_100G_0dB.txt"
p3_odd_trace_0dB = "D:\\project\\OFP2\\2018-04-27 WSS\\2019-06-19 data\\9H1370432\\f_100G\\port3\\f_ODD_100G_0dB.txt"

p3_even_trace_5dB = "D:\\project\\OFP2\\2018-04-27 WSS\\2019-06-19 data\\9H1370432\\f_100G\\Port3\\f_EVEN_100G_5dB.txt"
p3_odd_trace_5dB = "D:\\project\\OFP2\\2018-04-27 WSS\\2019-06-19 data\\9H1370432\\f_100G\\Port3\\f_ODD_100G_5dB.txt"

p3_even_trace_10dB = "D:\\project\\OFP2\\2018-04-27 WSS\\2019-06-19 data\\9H1370432\\f_100G\\Port3\\f_EVEN_100G_10dB.txt"
p3_odd_trace_10dB = "D:\\project\\OFP2\\2018-04-27 WSS\\2019-06-19 data\\9H1370432\\f_100G\\Port3\\f_ODD_100G_10dB.txt"

p3_even_trace_15dB = "D:\\project\\OFP2\\2018-04-27 WSS\\2019-06-19 data\\9H1370432\\f_100G\\Port3\\f_EVEN_100G_15dB.txt"
p3_odd_trace_15dB = "D:\\project\\OFP2\\2018-04-27 WSS\\2019-06-19 data\\9H1370432\\f_100G\\Port3\\f_ODD_100G_15dB.txt"

#add port4 data path
p4_even_trace_0dB = "D:\\project\\OFP2\\2018-04-27 WSS\\2019-06-19 data\\9H1370432\\f_100G\\port4\\f_EVEN_100G_0dB.txt"
p4_odd_trace_0dB = "D:\\project\\OFP2\\2018-04-27 WSS\\2019-06-19 data\\9H1370432\\f_100G\\port4\\f_ODD_100G_0dB.txt"

p4_even_trace_5dB = "D:\\project\\OFP2\\2018-04-27 WSS\\2019-06-19 data\\9H1370432\\f_100G\\Port4\\f_EVEN_100G_5dB.txt"
p4_odd_trace_5dB = "D:\\project\\OFP2\\2018-04-27 WSS\\2019-06-19 data\\9H1370432\\f_100G\\Port4\\f_ODD_100G_5dB.txt"

p4_even_trace_10dB = "D:\\project\\OFP2\\2018-04-27 WSS\\2019-06-19 data\\9H1370432\\f_100G\\Port4\\f_EVEN_100G_10dB.txt"
p4_odd_trace_10dB = "D:\\project\\OFP2\\2018-04-27 WSS\\2019-06-19 data\\9H1370432\\f_100G\\Port4\\f_ODD_100G_10dB.txt"

p4_even_trace_15dB = "D:\\project\\OFP2\\2018-04-27 WSS\\2019-06-19 data\\9H1370432\\f_100G\\Port4\\f_EVEN_100G_15dB.txt"
p4_odd_trace_15dB = "D:\\project\\OFP2\\2018-04-27 WSS\\2019-06-19 data\\9H1370432\\f_100G\\Port4\\f_ODD_100G_15dB.txt"



sys.path.append(component_path)
from WSS import WSS

grid_50 = np.linspace(1,96,96,dtype=np.int32)
grid_100 = np.linspace(1,48,48,dtype=np.int32)

sp_pass  =10+25
sp_block = 10+25
grid_50G = 50
grid_100G = 100




#print("chn\t","freq\t","wavelength\t",
#      "IL_cen\t","IL_best\t","IL_worst\t","IL_ripple\t",
#      "db_5p\t","ccp_5\t",
#      "db_1p\t","ccp_1\t",
#      "db_3p\t","ccp_3\t",    
#      "freq_shift\t",
#      "pdl\t","pmd\t","cd\t","gdr\t",
#      "ER_avg\t", "ER_sop")




def testWss(channel_plan, even_trace, odd_trace, sp_pass, sp_block, grid):
    for i in grid_100:
        chx = WSS(i, channel_plan, even_trace, odd_trace, sp_pass, sp_block, grid)
        parameter = chx.channel_parameter()
        
        AA = []
        
        chn = parameter[0]
        freq = parameter[1]
        wavelength = parameter[2]
    
        IL = chx.IL()
        IL_cen = IL[0]
        IL_best = IL[1]
        IL_worst = IL[2]
        IL_ripple = IL[3]
    
        db_5 = chx.passband(0.5)
        db_5p = db_5[6]
        ccp_5 = db_5[7]
    
        db_1 = chx.passband(1)
        db_1p = db_1[6]
        ccp_1 = db_1[7]
    
        db_3 = chx.passband(3)
        db_3p = db_3[6]
        ccp_3 = db_3[7]
    
        freq_shift = db_3[8]

        pdl = chx.pdl
        pmd = chx.pmd
    
        gdr = chx.gdr_cd(2)
        cd = gdr[0]
        gdr_1 = gdr[1]
    
        ER = chx.ER()
        ER_avg = ER[0]
        ER_sop = ER[1]
            
        AA.append(chn) 
        AA.append(freq)
        AA.append(wavelength)
        AA.append(IL_cen)
        AA.append(IL_best)
        AA.append(IL_worst)
        AA.append(IL_ripple)
        AA.append(db_5p)
        AA.append(ccp_5)
        AA.append(db_1p)
        AA.append(ccp_1)
        AA.append(db_3p)
        AA.append(ccp_3)
        AA.append(freq_shift)
        AA.append(pdl)
        AA.append(pmd)
        AA.append(cd)
        AA.append(gdr_1)
        AA.append(ER_avg)
        AA.append(ER_sop)
        
        AA = [str(x) for x in AA]
        
        for data in AA:
            with open('wss_result.txt','a') as f:
                f.writelines(data)
                f.writelines('\t')
        with open('wss_result.txt','a') as f:
            f.writelines('\n')







#port1
start = time.time()
print("--------------------------------------------------------------------------------------------")
print("------------------------------------Port1 test----------------------------------------------")
print("--------------------------------------------------------------------------------------------")

print("Port1 0dB test\n")
testWss(channel_plan_path, p1_even_trace_0dB, p1_odd_trace_0dB, sp_pass, sp_block, grid_100G)
print("--------------------------------------------------------------------------------------------")


print("Port1 5dB test\n")
testWss(channel_plan_path, p1_even_trace_5dB, p1_odd_trace_5dB, sp_pass, sp_block, grid_100G)
print("--------------------------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------------------")

print("Port1 10dB test\n")
testWss(channel_plan_path, p1_even_trace_10dB, p1_odd_trace_10dB, sp_pass, sp_block, grid_100G)
print("--------------------------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------------------")

print("Port1 15dB test\n")
testWss(channel_plan_path, p1_even_trace_15dB, p1_odd_trace_15dB, sp_pass, sp_block, grid_100G)
print("--------------------------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------------------")



#port2

print("--------------------------------------------------------------------------------------------")
print("------------------------------------Port2 test----------------------------------------------")
print("--------------------------------------------------------------------------------------------")

print("Port2 0dB test\n")
testWss(channel_plan_path, p2_even_trace_0dB, p2_odd_trace_0dB, sp_pass, sp_block, grid_100G)
print("--------------------------------------------------------------------------------------------")


print("Port2 5dB test\n")
testWss(channel_plan_path, p2_even_trace_5dB, p2_odd_trace_5dB, sp_pass, sp_block, grid_100G)
print("--------------------------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------------------")

print("Port2 10dB test\n")
testWss(channel_plan_path, p2_even_trace_10dB, p2_odd_trace_10dB, sp_pass, sp_block, grid_100G)
print("--------------------------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------------------")

print("Port2 15dB test\n")
testWss(channel_plan_path, p2_even_trace_15dB, p2_odd_trace_15dB, sp_pass, sp_block, grid_100G)
print("--------------------------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------------------")


#port3

print("--------------------------------------------------------------------------------------------")
print("------------------------------------Port3 test----------------------------------------------")
print("--------------------------------------------------------------------------------------------")

print("Port3 0dB test\n")
testWss(channel_plan_path, p3_even_trace_0dB, p3_odd_trace_0dB, sp_pass, sp_block, grid_100G)
print("--------------------------------------------------------------------------------------------")


print("Port3 5dB test\n")
testWss(channel_plan_path, p3_even_trace_5dB, p3_odd_trace_5dB, sp_pass, sp_block, grid_100G)
print("--------------------------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------------------")

print("Port3 10dB test\n")
testWss(channel_plan_path, p3_even_trace_10dB, p3_odd_trace_10dB, sp_pass, sp_block, grid_100G)
print("--------------------------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------------------")

print("Port3 15dB test\n")
testWss(channel_plan_path, p3_even_trace_15dB, p3_odd_trace_15dB, sp_pass, sp_block, grid_100G)
print("--------------------------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------------------")




#port4 test

print("--------------------------------------------------------------------------------------------")
print("-----------------------------------Port4 test-----------------------------------------------")
print("--------------------------------------------------------------------------------------------")


print("Port4 0dB test\n")
testWss(channel_plan_path, p4_even_trace_0dB, p4_odd_trace_0dB, sp_pass, sp_block, grid_100G)
print("--------------------------------------------------------------------------------------------")


print("Port4 5dB test\n")
testWss(channel_plan_path, p4_even_trace_5dB, p4_odd_trace_5dB, sp_pass, sp_block, grid_100G)
print("--------------------------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------------------")

print("Port4 10dB test\n")
testWss(channel_plan_path, p4_even_trace_10dB, p4_odd_trace_10dB, sp_pass, sp_block, grid_100G)
print("--------------------------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------------------")

print("Port4 15dB test\n")
testWss(channel_plan_path, p4_even_trace_15dB, p4_odd_trace_15dB, sp_pass, sp_block, grid_100G)
print("--------------------------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------------------")


stop = time.time()
print (stop - start)  



