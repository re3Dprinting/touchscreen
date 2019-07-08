from socket import *
import time
import serial
import serial.tools.list_ports
import g_serial
import sys
import json
 
host = "192.168.1.211" 
port = 63200
baudrate = 250000
serverconnected = False
serialconnected = False

class rpiclient(socket):
	def __init__(self, host, port):
		try:
			socket.__init__(self,AF_INET,SOCK_STREAM)
			self.connect((host,port))
			self.serial = None
			#First packet is Server Confirmation 
			confirm = self.recvdata()
			print confirm
			#Send Connection Confirmation
			self.senddata("Client Confirmed Connection\n")
			self.is_conn = True
		except error, exc:
			print "Error Connecting to Server: ", exc
			self.is_conn = False

	def attemptconnect(self, host, port):
		self.__init__(host, port)


	#senddata function converts data into json string then encodes it
	#Data is sent if the msg is not 0
	def senddata(self, msg):
		if msg:
			temp = json.dumps(msg).encode("base64")
			self.send(temp)
			self.recvdata() #Wait for ACK message
	def recvdata(self):
		data = self.recv(1024)
		while(len(data) == 0):
			data = self.recv(1024)
		if data:
			m_data = json.loads(data.decode("base64"))
			if(m_data == "OK"): print "Server ACK"
			else: return m_data



if __name__ == "__main__":
	#connect to the server
	g_client= rpiclient("192.168.1.211",63200)

	serial_conn = g_serial.serialconn()

	#Send server a notification that client is waiting for Gigabot seriall connection.

	#Send Header data if both serial and server are connected
	if g_client.is_conn and serial_conn.is_open:
		g_client.senddata(serial_conn.header)

	while True:
		time.sleep(1)

		#Conditional statement if one or both of the Server and Serial is disconnected.
		if(not (g_client.is_conn and serial_conn.is_open) ):
			#If either one is disconnected, attempt to connect.
			if not g_client.is_conn: g_client.attemptconnect("192.168.1.211",63200)
			if not serial_conn.is_open: serial_conn.attemptconnection()

			#The instant both become connected, send the header to the server.
			if(g_client.is_conn and serial_conn.is_open): 
				g_client.senddata(serial_conn.header)

		if(serial_conn.is_open):
			try:
				d = serial_conn.readdata()
				if g_client.is_conn: g_client.senddata(d)

			except error, exc:
				g_client.is_conn = False
				print "Server Disconnected!"
			except IOError:
				serial_conn.is_open = False
				print "Serial Disconnected!\n"
	print "program ended"

	# conn.close()
