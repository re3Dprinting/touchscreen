from socket import *
from g_data import *
import time
from serial import Serial
import serial.tools.list_ports
import json
import threading

#	g_serial class inherits from Serial object
class g_serial(Serial):
	def __init__(self,data_obj):
#	Reuse the dataobj is the same gigabot connects.
		self.data = data_obj
		self.data.serial = self
		self.com = None
		self.is_open = False

#	Function to Catch Exceptions for the g_serial 
	def catch_except(self, function):
		try:
			function()
			return
		except IOError, e:
			self.is_open = False
			self.data.changestatus("OF")
			return(self.com+ " Disconnected: "+ str(e))
		except ValueError,e:
			#print "COM port is unavalible/ or run program with root permission."
			#print "Retrying in 5 seconds"
			self.is_open = False
			self.data.changestatus("OF")
			return("ValueError :"+ str(e))
		except Exception, e:
			self.is_open = False
			return("Exception Error :"+ str(e))

#	COM list consists of attributes, device and description
	def scan(self):
		return list(serial.tools.list_ports.comports())

#	Attempt to reconnect to Serial
	def attemptconnect(self):
		err = self.catch_except(self.connect)
		if not err: return "Connection to"+ self.com+ " successful"
		else: return err

#	Initial attempt to connect to server			
	def connect(self):
		Serial.__init__(self, self.com, baudrate= 250000)
		#Set the status of the printer to ON
		self.reset()
		self.is_open = True
		
		#time.sleep(3)
	def reset(self):
		self.setDTR(False)
		time.sleep(0.4)
		self.flushInput()
		self.setDTR(True)
		self.data.counter[0] = 10
		self.data.changestatus("ON")


	def disconnect(self):
		if self.is_open:
			self.close()
			self.is_open = False
			return self.com+ " Disconnected!"
		else: return "No connected device"

	def initserial(self):
		#Extract Header information from the first few bytes of data
		self.readdata()
		self.en_reporttemp_stat()

#	Enable temperature reporting every 5 seconds through M155 S5
#	Retrieve printer stat through M78 gcode	
	def en_reporttemp_stat(self):
		#send to serial a M155 code to enable temperture reportings every 5s
		#self.send_serial('M155 S0.2')
		#Print Job status
		self.send_serial('M78')
		#Get current position 
		self.send_serial('M114')

	def send_serial(self, gcode):
		if self.is_open:
			print "SEND: " + gcode
			self.write((gcode+'\r').encode('utf-8'))
		else:
			print "Serial port is not open"

#	Read serial data function
#	If the insize is detected, wait half a second for the full transmission to come through
#	After recieving the data, parse it with the data object
	def readdata(self):
		 return self.catch_except(self.read_d)
	def read_d(self):
		insize = self.inWaiting()
		if insize: 
			time.sleep(0.5)
			insize = self.inWaiting()
			print "Bytes from Serial: ",insize
			serial_recv= self.read(insize)
			print(serial_recv)
			msg = self.data.parsedata(insize,serial_recv)


