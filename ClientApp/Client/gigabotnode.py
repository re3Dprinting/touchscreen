from __future__ import print_function
from __future__ import absolute_import
from builtins import object
import time
import serial
import serial.tools.list_ports
from .g_serial import * 
from .g_client import *
from .g_data import * 
import sys
import threading
import os
 

baudrate = 250000

class mainhandler(object):
	def __init__(self, clientconn, serialconn, data_o):
		self.clientconn = clientconn
		self.serialconn = serialconn
		self.datathread = data_o
#	Start Datathread to initialize timers
		self.datathread.start()
	
	def send_to_server(self):
		self.clientconn.senddata(self.datathread.buffer)
		self.datathread.buffer.clear()
		self.datathread.sendflag = False

#	Main loop for the Gigabotnode to read/ send data
	def loop(self):
#		Conditional statement if one or both of the Server and Serial is disconnected.
		if(not (self.clientconn.is_conn and self.serialconn.is_open) ):
#			If either one is disconnected, attempt to connect.
			if self.datathread.reconnflag:
				self.clientconn.attemptconnect(self.datathread)
				self.serialconn.attemptconnect(self.datathread)
				self.datathread.reconnflag = False
#			The instant both become connected, send the header to the server.
			if(self.clientconn.is_conn and self.serialconn.is_open):
				self.datathread.buffer.clear()
				self.datathread.addtobuffer("HD",self.datathread.header)
				self.datathread.addtobuffer("SS",self.datathread.stats)
				self.datathread.addtobuffer("ST",self.datathread.status)
				self.datathread.addtobuffer("FI", self.datathread.currentfile)
				self.send_to_server()

		if self.serialconn.is_open: 
			self.serialconn.readdata()
		if self.datathread.start_timeout_seq and self.clientconn.is_conn: 
			#print "pinging"
			self.send_to_server()

		elif self.clientconn.is_conn and self.datathread.sendflag: 
			#print "sendflag"
			self.send_to_server()

if __name__ == "__main__":
	os.system("clear")
#	Attempt to Initialize the Client Connection, Data Object, and Serial Connection.
	data_thread = g_data()
	client_conn= g_client(data_thread)
	serial_conn = g_serial(data_thread)

#	Create mainhandler object
	mainhand = mainhandler(client_conn, serial_conn, data_thread)

	while True:
		time.sleep(1)
		mainhand.loop()

	print("program ended")

	# conn.close()







	# def ex_wrap(self, function):
	# 	try:
	# 		function()
	# 	except error, e:
	# 		print e.args[0]
	# 		if e.args[0] == errno.EAGAIN or e.args[0] == errno.EWOULDBLOCK:
	# 			print "nope no data"
	# 		if e.args[0] == 32 or e.args[0] == 104:
	# 			self.clientconn.is_conn = False
	# 			print "Server Disconnected!"
	# 	except IOError:
	# 		self.serialconn.is_open = False
	# 		self.datathread.changestatus("OF")
	# 		print "Serial Disconnected!\n"
	# def attempt_transfer_header(self):
	# 	if self.clientconn.is_conn and self.serialconn.is_open:
	# 		self.clientconn.senddata(self.serialconn.header)
	# class SenderThread(threading.Thread):
	# _stop = False
	# def __init__(self, clientconn, data_obj):
	# 	super(SenderThread,self).__init__()
	# 	self.clientconn = clientconn
	# 	self.data_obj = data_obj
	# 	self.counter = 0
	# def stop(self):
	# 	self._stop = True
	# def run(self):
	# 	while self._stop == False:
	# 		self.counter += 1
	# 		time.sleep(1)
	# 		if self.counter >= 5:
	# 			msg = self.data_obj.buffer
	# 			print "MSG: ",msg
	# 			try:
	# 				if self.clientconn.is_conn: self.clientconn.senddata(msg)
	# 			except error, exc:
	# 				self.clientconn.is_conn = False
	# 				print "Server Disconnected!"
	# 			#clear the buffer after data is sent
	# 			self.data_obj.buffer.clear()
	# 			self.counter = 0