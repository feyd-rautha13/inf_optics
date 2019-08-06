###########################
# This VOA control is based on VIAVI MAP200 Platform
# Author:	Kunjen Zhang
# Date:		2017-06-09
###########################

import sys
import telnetlib
import time


class voa_sha:
    def __init__(self, ip, port):
        self.tln = telnetlib.Telnet(ip, int(port), timeout=10)
        # self.tln.set_debuglevel(2)

    def set_att_value(self, dB):
        timeout = 10
        for n in range(0, timeout):
            self.cmdSet("output:attenuation 1, {0}".format(str(dB)))
            time.sleep(1)
            ret = self.cmdGet("output:attenuation? 1")
            ret = float(ret)
            if abs(ret - dB) < 0.001:
                print "Attenuation has been set to {0}dB".format(str(ret))
                break
            elif n == timeout - 1:
                print "Error!! Set the attenuation to {0}dB fail.".format(str(dB))
                print "Get current attenuation value is {0}dB".format(ret)
                sys.exit(1)

    def setShutterOff(self):
        self.set_att_value(30)

    def read_att_value(self):
        ret = self.cmdGet("output:attenuation? 1")
        ret = float(ret)
        return ret

    def cmdSet(self, cmd):
        self.tln.write("{0}\n".format(cmd))
        time.sleep(0.2)
        ret = self.cmdGet("*esr?")
        if int(ret) != 0:
            print "Get ESR value: {0}".format(ret)
            print "Error!! Command \"{0}\" send fail.".format(cmd)
            sys.exit(1)

    def cmdGet(self, cmd):
        self.tln.write("{0}\n".format(cmd))
        ret = self.tln.read_until("\n")
        ret = ret.replace("\n", "")
        return ret

    def closeConnection(self):
        self.tln.close()

    def setShutterOff(self):
        pass


if __name__ == '__main__':
    voa_inst = voa_sha('172.29.153.180', 8005)
    print(voa_inst.set_att_value(30.0))
