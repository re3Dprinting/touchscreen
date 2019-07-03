from socket import *
import time
from serial import Serial
import serial.tools.list_ports
import json


#Inheriting from the Serial class
class serialconn(Serial):
	def __init__(self):
		com = list(serial.tools.list_ports.comports())
		for p in com:
			if "/dev/ttyUSB" in p.device:
				com = p.device
		try:
			Serial.__init__(self,com, baudrate= 250000)
			self.setDTR(False)
			time.sleep(1)
			self.flushInput()
			self.setDTR(True)
			self.data = serialdata()
			time.sleep(3)
		except:
			print "COM port is unavalible/ or run program with root permission."
			time.sleep(3)

	def attemptconnection(self):
		while not self.is_open: serial_conn = self.__init__()
	
	def connect_to_bot(self):
		print("SEND: M155 S5\r")
		#send to serial a M155 code to enable temperture reportings every 5s
		self.write('M155 S5\r'.encode('utf-8'))
		time.sleep(1)
		

	def readdata(self):
		insize = self.inWaiting()
		if insize: time.sleep(0.5)
		insize = self.inWaiting()
		print "Bytes from Serial: ",insize
		serial_recv= self.read(insize)
		print(serial_recv)
		msg = self.data.parsedata(insize, serial_recv)
		return msg

		

class serialdata:
	def __init__(self):
		self.temp = dict()
		self.uploaddate= ""
		self.model = ""

	def extracttemp(self,variable,data):
		#Extracting temperature data to a tuple in the format (Temp/SetTemp)
		if variable in data:
			start = end = data.find(variable) + len(variable)
			while((ord(data[end]) < 58 and ord(data[end])>45) or ord(data[end]) == 32): end+=1
			tup = [float(x) for x in data[start:end].split("/")]
			self.temp[variable[:-1]] = tup
	def extractheader(self, data):
		#Searching for last updated timestamp
		start = end = data.find("Last Updated:") + len("Last Updated:")
		while(ord(data[end]) != 124): end += 1
		self.uploaddate = data[start:end].strip()
		#print self.uploaddate
		start = end
		#Increment until you hit "G" for GB
		while(ord(data[start]) != 66): start += 1
		end = start
		while(ord(data[end]) != 86): end += 1
		modstring = data[start+1:end].strip()
		if("3" in modstring): self.model = "Regular"
		else: self.model = modstring
		#print self.model

	def parsedata(self,msglen, data):
		data = data.decode("utf-8")
		if(msglen <200 and 'T' in data):
			self.extracttemp("T0:", data)
			self.extracttemp("T1:", data)
			self.extracttemp("B:", data)
			return self.temp
		if(msglen >200 and "Updated" in data):
			self.extractheader(data)
			return self.uploaddate + "|" + self.model


# if __name__ == "__main__":
# 	x = gigabotconnection()
# 	data = b' T:178.41 /180.00 B:59.39 /60.00 T0:178.41 /180.00 T1:26.31 /0.00 @:92 B@:127 @0:92 @1:0\n'
# 	decode = data.decode('utf-8')
# 	print(decode)
# 	x.parsedata(decode)
# 	print(x.temp)


