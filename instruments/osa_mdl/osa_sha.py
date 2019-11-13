###########################
# This OSA control is based on VIAVI MTS8000 Platform
# Author:	Kunjen Zhang
# Date:		2017-06-09
###########################

import sys
import telnetlib
import time


class osa_sha:
    def __init__(self, ip, port):
        self.tln = telnetlib.Telnet(ip, int(port), timeout=10)
        # self.tln.set_debuglevel(2)
        self.cmdSet("*rem")
        while True:
            ret = self.cmdGet("status:acq?")
            if ret != "STOPPED":
                self.cmdSet("key start")
            else:
                break

        self.cmdSet("osasetup:mode 1")
        self.cmdSet("osasetup:avg NO")

    def sweep(self):
        pass

    def getOSNR(self):
        self.cmdSet("key start")
        time.sleep(1)
        while True:
            ret = self.cmdGet("status:acq?")
            if ret == "STOPPED":
                break
            else:
                time.sleep(1)

        ret = self.cmdGet("table:line? 1")
        # print ret
        ret = ret.split(",")
        osnr = float(ret[5])
        print "Current OSNR is {0}dB.".format(str(osnr))
        return osnr

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

    def close(self):
        while True:
            ret = self.cmdGet("status:acq?")
            if ret != "STOPPED":
                self.cmdSet("key start")
            else:
                break

        self.cmdSet("osasetup:mode 0")
        self.cmdSet("osasetup:avg NO")
        self.cmdSet("key start")

        self.tln.close()


if __name__ == '__main__':
    osa_inst = osa_sha('172.29.153.181', 8002)
    print(osa_inst.getOSNR())
