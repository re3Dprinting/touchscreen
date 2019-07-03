from socket import *
import time
import serial
import serial.tools.list_ports
import g_serial
import sys
import json

baudrate = 250000

class rpiclient(socket):
	def __init__(self, host, port):
		socket.__init__(self,AF_INET,SOCK_STREAM)
		self.connect((host,port))
		self.serial = None
		data = self.recv(1024)
		
		self.waitforACK()

		self.send("Client Confirmed Connection\n")
	def senddata(self, msg):
		if msg:
			temp = json.dumps(msg).encode("base64")
			self.send(temp)
	def waitforACK(self):
		data = self.recv(1024)
		while(len(data) == 0):
			data = self.recv(1024)



if __name__ == "__main__":
	#connect to the server
	g_client= rpiclient("192.168.1.49",63200)


	serial_conn = g_serial.serialconn()

	#Send server a notification that client is waiting for Gigabot connection.
	#if not serial_conn.is_open: g_client
	serial_conn.attemptconnection()

	#Extract Header information from the first few bytes of data
	header = serial_conn.readdata()
	g_client.senddata(header)
	g_client.waitforACK()

	serial_conn.connect_to_bot()

	while True:
		time.sleep(1)
		try:
			d = serial_conn.readdata()
			g_client.senddata(d)
			g_client.waitforACK()
			
		except IOError:
			print "Device Disconnected!\n"
			break
	print "program ended"

	# conn.close()
