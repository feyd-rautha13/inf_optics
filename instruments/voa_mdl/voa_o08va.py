import subprocess, re, os
setstr = 'attenuation to (.*) dB \(requested'
readstr = 'Attenuation .*:(.*)'

class voa_o08va:
    def __init__(self, IP, IP_Port, card_port, password='vin7ageP0rt#'):
        print('O08VA init')

        #card port in the range of [0, 7]
        self.port = card_port

        # Login to card using PLink
        user = '-l root -pw ' + password
        login = "plink {0:s} -P {1:d} -{2:s} {3:s}".format(IP, IP_Port, 'ssh', user)
        self.sp = subprocess.Popen(login, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        print("Connected to %s" % IP)

        self.currentValues = self.read_att_value()

    def read_att_value(self):
        res = float(self.Cli('cli att {0:d}'.format(self.port), readstr))
        print(self.__class__.__name__ + ' has value %s' % res)
        return res

    def set_att_value(self, val):
        self.write('cli att {0:d} {1:.1f}'.format(self.port, val))
        self.currentValues = val
        print(self.__class__.__name__ + ' P%d is setting value to %.2f' % (self.port, val))

    def closeConnection(self):
        self.write("exit")
        print(self.__class__.__name__ + 'stopped')

    def setShutterOn(self):
        self.set_att_value(self.currentValues)
        print(self.__class__.__name__ + 'Shutter on')

    def setShutterOff(self):
        self.set_att_value(20.0)
        print(self.__class__.__name__ + 'Shutter off')

    def write(self, command):
        self.sp.stdin.write(command + '\n')

    def Cli(self, command, searchstring):
        self.write(command)
        A = None
        while not A:
            s = self.sp.stdout.readline()
            # print s
            A = re.search(searchstring, s)  # wait for string
        return A.group(1)  # return receive string


if __name__ == '__main__':
    voa_port = 0
    IP = "10.50.23.179"

    voa_inst_p0 = voa_o08va(IP, 22, voa_port)
    voa_inst_p0.set_att_value(20)
    voa_inst_p0.read_att_value()