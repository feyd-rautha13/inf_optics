# /usr/bin/env python
# -*- coding : utf-8 -*-

__author__ = 'Sizhan Liu'
__version__ = "1.0"

'''
This script is used to convert Luna result to numpy parse.
'''

import os
keyword_1 = 'mux'
keyword_2 = 'txt'
output_path = 'C:\\Data\\sliu3\\Documents\\work\\coding\\python\\OpticalTest\\OMD64\\demux_data\\'

def file_convert():
    all_file_list = os.listdir()
    file_list_tmp_1 = [x for x in all_file_list if keyword_1 in x]
    file_list_tmp_2 = [x for x in file_list_tmp_1 if keyword_2 in x]
    
    #data_name = [x.relpace('.txt',"") for x in file_list_tmp_2]
    
    for i in file_list_tmp_2:
        with open(i,'r') as f:
            line_list = f.readlines()
        
        del line_list[0:8]
        output_file_name ='f_' + i
        
        file_output = open(output_path + output_file_name, 'w')
        file_output.writelines(line_list)
        file_output.close()
        print ('file convert for',i, "is finished.")


if __name__ == '__main__':
    file_convert()

