from socket import *
from g_data import *
import time
from serial import Serial
import serial.tools.list_ports
import json


#Inheriting from the Serial class
class g_serial(Serial):
	def __init__(self,data_obj):
		com = list(serial.tools.list_ports.comports())
		self.data = data_obj
		for p in com:
			if "/dev/ttyUSB" in p.device:
				com = p.device
		try:
			Serial.__init__(self,com, baudrate= 250000)
			#Set the status of the printer to ON
			self.data.changestatus("ON")
			self.setDTR(False)
			time.sleep(1)
			self.flushInput()
			self.setDTR(True)
			time.sleep(3)
			#Extract Header information from the first few bytes of data
			self.header = self.readdata()
			self.en_reporttemperture()
		except ValueError:
			print "COM port is unavalible/ or run program with root permission."
			self.data.changestatus("OF")
			time.sleep(3)

	def attemptconnection(self,data):
		self.__init__(data)
	
	def en_reporttemperture(self):
		print("SEND: M155 S5\r")
		#send to serial a M155 code to enable temperture reportings every 5s
		self.write('M155 S5\r'.encode('utf-8'))
		time.sleep(1)
		
	def readdata(self):
		insize = self.inWaiting()
		if insize: 
			time.sleep(0.5)
			insize = self.inWaiting()
			print "Bytes from Serial: ",insize
			serial_recv= self.read(insize)
			print(serial_recv)
			msg = self.data.parsedata(insize,serial_recv)
			return msg

# if __name__ == "__main__":
# 	x = gigabotconnection()
# 	data = b' T:178.41 /180.00 B:59.39 /60.00 T0:178.41 /180.00 T1:26.31 /0.00 @:92 B@:127 @0:92 @1:0\n'
# 	decode = data.decode('utf-8')
# 	print(decode)
# 	x.parsedata(decode)
# 	print(x.temp)


