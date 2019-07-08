from socket import *
import time
import serial
import serial.tools.list_ports
import g_serial
import g_client
import sys
import json
 
host = "192.168.1.211" 
port = 63200
baudrate = 250000
serverconnected = False
serialconnected = False

class mainhandler():
	def __init__(self, clientconn, serialconn):
		self.clientconn = clientconn
		self.serialconn = serialconn
	def attempt_transfer_header():
		try:
			if client_conn.is_conn and serial_conn.is_open:
				client_conn.senddata(serial_conn.header)
		except error, exc:
			client_conn.is_conn = False
			print "Server Disconnected!"
		except IOError:
			serial_conn.is_open = False
			print "Serial Disconnected!\n"

if __name__ == "__main__":
	#connect to the server
	client_conn= g_client("192.168.1.211",63200)
	serial_conn = g_serial.serialconn()

	mainhand = mainhandler(client_conn, serial_conn)

	#Send Header data if both serial and server are connected
	mainhand.attempt_transfer_header()

	while True:
		time.sleep(1)
		try:
			#Conditional statement if one or both of the Server and Serial is disconnected.
			if(not (client_conn.is_conn and serial_conn.is_open) ):
				#If either one is disconnected, attempt to connect.
				if not client_conn.is_conn: client_conn.attemptconnect("192.168.1.211",63200)
				if not serial_conn.is_open: serial_conn.attemptconnection()
				#The instant both become connected, send the header to the server.
				if(client_conn.is_conn and serial_conn.is_open): glient._connsenddata(serial_conn.header)

			if client_conn.is_conn and not serial_conn.is_open:
				#Send OFF/Disconnected status to server
				pass

			if not client_conn.is_conn and serial_conn.is_open:

				d = serial_conn.readdata()

			elif client_conn.is_conn and serial_conn.is_open:
				d = serial_conn.readdata()
				client_conn.senddata(d)
		except error, exc:
			client_conn.is_conn = False
			print "Server Disconnected!"
		except IOError:
			serial_conn.is_open = False
			print "Serial Disconnected!\n"

	print "program ended"

	# conn.close()
