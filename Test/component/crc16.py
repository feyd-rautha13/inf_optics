def crc16(x, invert):
    a = 0xFFFF
    b = 0xA001
    for byte in x:
        a ^= ord(byte)

        for i in range(8):
            last = a % 2
            a >>= 1
            if last == 1:
                a ^= b
    s = hex(a).upper()
    
    return s[4:6]+s[2:4] if invert == True else s[2:4]+s[4:6]

import openpyxl
path = "D:\\project\\pluggable\\400G\\400G EEPROM\\QSFP-DD EEPROM Spec-Mar25.xlsx"



def get_list(path, sh_order):
    wb = openpyxl.load_workbook(path)
    sheet = wb[wb.sheetnames[sh_order]]
    s=[]
    string = ''
    for i in range(2,120):
        addr = 'G'+str(i)
        s.append(str(sheet[addr].value))
    for i in s:
        string += i
    wb.close()
    return string

def inf_crc16(data):
    length = int(len(data)/2)
    crc = 0xffff
    for i in range(length):
        flag = int(data[2*i:2*i+2],16)
        crc ^= flag
        for i in range(8):
            last = crc%2
            crc >>= 1
            if last==1:
                crc ^= 0xa001
    return hex(crc)

'''
MSB LSB 应该交换
'''

data = '00123456789ABCDE'
inf_crc16(data)




'''
	常用查表法和计算法。计算方法一般都是：
（1）、预置1个16位的寄存器为十六进制FFFF（即全为1），称此寄存器为CRC寄存器；
（2）、把第一个8位二进制数据（既通讯信息帧的第一个字节）与16位的CRC寄存器的低
       8位相异或，把结果放于CRC寄存器，高八位数据不变；
（3）、把CRC寄存器的内容右移一位（朝低位）用0填补最高位，并检查右移后的移出位；
（4）、如果移出位为0：重复第3步（再次右移一位）；如果移出位为1，CRC寄存器与多

    项式A001（1010 0000 0000 0001）进行异或；
（5）、重复步骤3和4，直到右移8次，这样整个8位数据全部进行了处理；
（6）、重复步骤2到步骤5，进行通讯信息帧下一个字节的处理；
（7）、将该通讯信息帧所有字节按上述步骤计算完成后，得到的16位CRC寄存器的高、低
       字节进行交换；
（8）、最后得到的CRC寄存器内容即为：CRC码。
	'''