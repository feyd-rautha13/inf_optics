# /usr/bin/env python
# -*- coding : utf-8 -*-

__author__ = 'Sizhan Liu'
__version__ = "1.0"

'''
This script is used to convert Luna result to numpy parse.
'''

import os

#raw_data_path = "D:\\project\\2018-07-09 OMD64\\2019-01-24 P1 update\\raw data\\mux\\"
#output_path = 'D:\\project\\2018-07-09 OMD64\\2019-01-24 P1 update\\raw data\\f_mux\\'

raw_data_path = "D:\\project\\OFP2\\2018-04-27 WSS\\2019-04-12 data\\9H0320002\\50G\\port4\\"
output_path = "D:\\project\\OFP2\\2018-04-27 WSS\\2019-04-12 data\\9H0320002\\f_50G\port4\\"


def file_convert():
    file_name_list = os.listdir(raw_data_path)
    file_name_list = [x for x in file_name_list if 'txt' in x]
    file_name_list_0 = [raw_data_path+i for i in file_name_list]

    
    #data_name = [x.relpace('.txt',"") for x in file_list_tmp_2]
    
    for i in range(len(file_name_list_0)):
        with open(file_name_list_0[i],'r') as f:
            line_list = f.readlines()
        
        del line_list[0:8]
        output_file_name ='f_' + file_name_list[i]
        
        file_output = open(output_path + output_file_name, 'w')
        file_output.writelines(line_list)
        file_output.close()
        print ('file convert for',file_name_list[i], "is finished.")

if __name__ == '__main__':
    file_convert()
