# -*- coding: utf-8 -*-

interface_path = 'D:\\work\\coding\\python\\inf_optics\\interface'
instument_path = "D:\\work\\coding\\python\\inf_optics\\labdevice"

import sys
sys.path.append(interface_path)
sys.path.append(instument_path)

from Telnetinterface import telnet
from ont600 import ONT600

#OSM-5q Serial Port
ip_1 = '172.29.150.197'
port_ip1_1 = 7100
port_ip1_2 = 7101

#OSM-5q TL1
ip_2 = '172.29.150.198'
port_ip2 = 3083

#ONT-603
ip_3 = '172.29.150.93'
port_1 = 11066


#mainf = ONT600_Mainframe(ip_3, 5001, 10)
ont = ONT600(ip_3, port_1, 10)

ont.query('*IDN?')






'''
osm5q = telnet(host = ip_1, port = port_ip1_2)


fq_prompt = 'OSM4:HALServer:20:1>'


def ModInfor():
    a =osm5q.query('qsfp 4 d', fq_prompt)

    a = a.decode()
    print(a)


def ModEq():
    osm5q.write('qsfp 4 r 0x3EA 6')
    a = osm5q.tn.read_until(fq_prompt, timeout=10)
    a = a.decode()
    return a

'''