from socket import *
import json
import errno

host = "192.168.1.169" 
port = 63200

#	The g_client class inherits from the socket class
class g_client(socket):
	def __init__(self):
		self.catch_except(self.connect)

	def connect(self):
		socket.__init__(self,AF_INET,SOCK_STREAM)
		self.connect((host,port))
		self.setblocking(False)
		self.serial = None
		#First packet is Server Confirmation 
		self.is_conn = True
		confirm = self.recvdata()
		print confirm
		#Send Connection Confirmation
		self.senddata("Client Confirmed Connection\n")

	def catch_except(self,function):
		try:
			function()
		except error, e:
			print e.args[0]
			if e.args[0] == errno.EAGAIN or e.args[0] == errno.EWOULDBLOCK:
				print "nope no data"
			if e.args[0] == 32 or e.args[0] == 104:
				self.is_conn = False
				print "Server Disconnected!"

#	Attempt to reconnect to Server
	def attemptconnect(self, host, port):
		if not self.is_conn: self.__init__(host, port)

#	senddata function converts data into json string then encodes it
#	If no data, send "None" msg to ping server. 
	def senddata(self, msg):
		temp = json.dumps(msg).encode("base64")
		self.send(temp)
		self.recvdata() #Wait for ACK message

#	recvdata waits for the server to acknowledge
#	Should close connection if timeout
#	IMPLEMENT TIMEOUT CODE HERE. SHOULD CLOSE IF TIMED OUT
	def recvdata(self):
		try:
			data = self.recv(1024)
			if data:
				m_data = json.loads(data.decode("base64"))
				if(m_data == "OK"): print "Server ACK"
				else: return m_data
		except error, e:
			print e
			if e.args[0] == errno.EAGAIN or e.args[0] == errno.EWOULDBLOCK:
				print "No data from read"

