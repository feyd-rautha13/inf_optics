###########################
# This OSA control is based on VIAVI MTS8000 Platform
# Author:	Youbin Zheng/Kunjen Zhang
# Date:		2018-12-25
###########################

import time
import sys
import telnetlib

class OSA:
	#def __init__(self, ip, port):
	def __init__(self, ip="172.29.150.154", port=8002):
		self.tln = telnetlib.Telnet(ip, int(port), timeout = 10)
		self.tln.set_debuglevel(2)
		self.Set("*rem")
		while True:
			ret = self.Get("status:acq?")
			if ret != b"STOPPED\n":
				self.Set("key start")
			else:
				break
		#self.cmdSet("osasetup:seacq full")  
		self.Set("osasetup:seacq cband")                
		self.Set("osasetup:mode 1")
		self.Set("osasetup:avg LOW")

	def getOsnr(self):
		self.Set("key start")
		time.sleep(1)
		while True:
			ret = self.cmdGet("status:acq?")
			if ret == b"STOPPED\n":
				break
			else:
				time.sleep(1)

		ret = self.Get("table:line? 1")
		print(ret)
		#ret = ret.split(",")
		ret = ret.decode('utf8').rstrip().split(",")
		osnr = float(ret[5])
		print("Current OSNR is {0}dB.".format(str(osnr)))
		return osnr

	def Set(self, cmd):
		cmd = str(cmd) + '\n'
		cmd = cmd.encode()
		self.tln.write(cmd)
		#self.tln.write("{0}\n".format(cmd))
		time.sleep(0.2)
		ret = self.Get("*esr?")
		if ret != b"0\n":
			print ("Get ESR value: {0}".format(ret))
			print ("Error!! Command \"{0}\" send fail.".format(cmd))
			sys.exit(1)
	
	def Get(self, cmd):
		cmd = str(cmd) + '\n'
		cmd = cmd.encode()
		self.tln.write(cmd)
		#self.tln.write("{0}\n".format(cmd))
		ret = self.tln.read_until(b"\n")
#		ret = ret.replace("\n", "")
		return ret
	
	def close(self):
		while True:
			ret = self.cmdGet("status:acq?")
			if ret != b"STOPPED\n":
				self.Set("key start")
			else:
				break

		self.Set("osasetup:mode 0")
		self.Set("osasetup:avg NO")
		self.Set("key start")

		self.tln.close()
