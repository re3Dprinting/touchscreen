from socket import *
from g_data import *
import time
from serial import Serial
import serial.tools.list_ports
import json

#	g_serial class inherits from Serial object
class g_serial(Serial):
	def __init__(self,data_obj):
#	If the gigabot is disconnected, keep the data object
#	Reinitialize the object if the gigabot is the same. 
		self.data = data_obj
		com = list(serial.tools.list_ports.comports())
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
			self.readdata()
			self.en_reporttemp_stat()
		except ValueError:
			print "COM port is unavalible/ or run program with root permission."
			print "Retrying in 5 seconds"
			self.data.changestatus("OF")

#	Attempt to reconnect to Serial Connection.
	def attemptconnection(self,data):
		if not self.is_open: self.__init__(data)

#	Enable temperature reporting every 5 seconds through M155 S5
#	Retrieve printer stat through M78 gcode	
	def en_reporttemp_stat(self):
		print("SEND: M155 S5\r")
		#send to serial a M155 code to enable temperture reportings every 5s
		self.write('M155 S5\r'.encode('utf-8'))
		time.sleep(1)
		self.write('M78\r'.encode('utf-8'))
		time.sleep(1)

#	Read serial data function
#	If the insize is detected, wait half a second for the full transmission to come through
#	After recieving the data, parse it with the data object
	def readdata(self):
		insize = self.inWaiting()
		if insize: 
			time.sleep(0.5)
			insize = self.inWaiting()
			print "Bytes from Serial: ",insize
			serial_recv= self.read(insize)
			print(serial_recv)
			msg = self.data.parsedata(insize,serial_recv)


