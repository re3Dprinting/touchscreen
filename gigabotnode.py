import time
import serial
import serial.tools.list_ports
from g_serial import * 
from g_client import *
from g_data import * 
import sys
import threading
 
host = "192.168.1.211" 
port = 63200
baudrate = 250000
serverconnected = False
serialconnected = False

class mainhandler():
	def __init__(self, clientconn, serialconn, data_o):
		self.clientconn = clientconn
		self.serialconn = serialconn
		self.data = data_o
		self.statusthread = SenderThread(self.clientconn, self.data)
		self.statusthread.start()
	
	def ex_wrap(self, function):
		try:
			function()
		except error, exc:
			self.clientconn.is_conn = False
			print "Server Disconnected!"
		except IOError:
			self.serialconn.is_open = False
			print "Serial Disconnected!\n"

	def attempt_transfer_header(self):
		if self.clientconn.is_conn and self.serialconn.is_open:
			# d = self.serialconn.readdata()
			# print(d)
			self.clientconn.senddata(self.serialconn.header)

	def loop(self):
		#Conditional statement if one or both of the Server and Serial is disconnected.
		if(not (self.clientconn.is_conn and self.serialconn.is_open) ):
			#If either one is disconnected, attempt to connect.
			if not self.clientconn.is_conn: self.clientconn.attemptconnect("192.168.1.211",63200)
			if not self.serialconn.is_open: self.serialconn.attemptconnection()
			#The instant both become connected, send the header to the server.
			if(self.clientconn.is_conn and self.serialconn.is_open): self.clientconn.senddata(self.serialconn.header)

		if self.clientconn.is_conn and not self.serialconn.is_open:
			#Set status of the printer to OFF
			self.data.status = "OF"

		if not self.clientconn.is_conn and self.serialconn.is_open:
			d = self.serialconn.readdata()

		elif self.clientconn.is_conn and self.serialconn.is_open:
			d = self.serialconn.readdata()
			#self.clientconn.senddata(d)

class SenderThread(threading.Thread):
	_stop = False
	def __init__(self, clientconn, data_obj):
		super(SenderThread,self).__init__()
		self.clientconn = clientconn
		self.data_obj = data_obj
	def stop(self):
		self._stop = True
	def run(self):
		counter = 0
		while self._stop == False:
			counter += 1
			time.sleep(1)
			if counter ==2:
				msg = self.data_obj.status
				print "Send data here" + msg
				self.clientconn.senddata("ST"+msg)
				counter = 0





if __name__ == "__main__":
	#connect to the server
	client_conn= g_client("192.168.1.211",63200)
	serial_conn = g_serial()
	data_obj = serial_conn.data

	mainhand = mainhandler(client_conn, serial_conn, data_obj)

	#Send Header data if both serial and server are connected
	mainhand.ex_wrap(mainhand.attempt_transfer_header)

	while True:
		time.sleep(1)
		mainhand.ex_wrap(mainhand.loop)

	print "program ended"

	# conn.close()
