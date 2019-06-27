from socket import *
import time
import serial
import serial.tools.list_ports

class gcodedata:
	def __init__(self):
		self.temp = dict()

	def extracttemp(self,variable,data):
		if variable in data:
			start= end= data.find(variable) + len(variable)
			while((ord(data[end])< 58 and ord(data[end])>45) or ord(data[end]) == 32): end+=1
			tup = [float(x) for x in data[start:end].split("/")]
			self.temp[variable[:-1]] = tup

	def parsedata(self,data):
		if('T' in data):
			self.extracttemp("T0:", data)
			self.extracttemp("T1:", data)
			self.extracttemp("B:", data)


# if __name__ == "__main__":
# 	x = gigabotconnection()
# 	data = b' T:178.41 /180.00 B:59.39 /60.00 T0:178.41 /180.00 T1:26.31 /0.00 @:92 B@:127 @0:92 @1:0\n'
# 	decode = data.decode('utf-8')
# 	print(decode)
# 	x.parsedata(decode)
# 	print(x.temp)


