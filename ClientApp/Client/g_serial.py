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
		self.just_open = True

#	Function to Catch Exceptions for the g_serial 
	def catch_except(self, function):
		try:
			function()
			return
		except IOError, e:
			self.is_open = False
			self.data.changestatus("OF")
			print e.args[0]
			return(self.com+ " Disconnected: "+ str(e))
		except ValueError,e:
			#print "COM port is unavalible/ or run program with root permission."
			#print "Retrying in 5 seconds"
			self.is_open = False
			self.data.changestatus("OF")
			return("ValueError :"+ str(e))
		except Exception, e:
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
		self.is_open = True
		self.reset()
		
#	Reset the machine, triggers the setDTR pin, 
#	Changes the status back to "ON"
#	Resets the Temperature window to not printing
	def reset(self):
		self.just_open = True
		self.data.counter[0] = 0
		self.setDTR(False)
		time.sleep(0.4)
		self.flushInput()
		self.setDTR(True)
		self.data.changestatus("ON")
		self.data.notprinting.emit("notprinting")
		print "RESET: ", self.just_open, " status: ", self.data.status
		# print "Reset?: ", self.just_open
		# print self.data.status

#	Disconnect closes the serial port
	def disconnect(self):
		if self.is_open:
			self.close()
			self.is_open = False
			self.data.changestatus("OF")
			return self.com+ " Disconnected!"
		else: return "No connected device"

#	Called after 10 seconds resetting the machine.
#	Extract Header information from the first few bytes of data
	def initserial(self):
		self.readdata()
		self.en_reporttemp_stat()

#	Enable temperature reporting every 5 seconds through M155 S5
#	Retrieve printer stat through M78 gcode	
	def en_reporttemp_stat(self):
		#send to serial a M155 code to enable temperture reportings every 5s
		#self.send_serial('M155 S1')
		self.send_serial("M27 S5")
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


