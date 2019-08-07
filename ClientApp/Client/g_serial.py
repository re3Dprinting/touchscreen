from socket import *
from g_data import *
import time
from serial import Serial
import serial.tools.list_ports
import json

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
			return e
		except ValueError:
			#print "COM port is unavalible/ or run program with root permission."
			#print "Retrying in 5 seconds"
			return "ValueError :", e
			self.data.changestatus("OF")
		except Exception, e:
			return "Exception Error :", e

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
		self.setDTR(False)
		time.sleep(0.1)
		self.flushInput()
		self.setDTR(True)
		self.data.changestatus("ON")
		self.is_open = True
		self.data.ser_conn = True
		self.data.counter[0] = 10
		#time.sleep(3)

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
		self.send_serial('M155 S1')
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
		self.catch_except(self.read_d)
	def read_d(self):
		insize = self.inWaiting()
		if insize: 
			time.sleep(0.5)
			insize = self.inWaiting()
			print "Bytes from Serial: ",insize
			serial_recv= self.read(insize)
			print(serial_recv)
			msg = self.data.parsedata(insize,serial_recv)


