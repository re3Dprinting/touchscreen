from socket import *
import json

#	The g_client class inherits from the socket class
class g_client(socket):
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

		#TRY TO CONNECT AGAIN IN 5 SECONDS.
		except error, exc:
			print "Error Connecting to Server: ", exc
			self.is_conn = False

#	Attempt to reconnect to Server
	def attemptconnect(self, host, port):
		self.__init__(host, port)

#	senddata function converts data into json string then encodes it
#	If no data, send "None" msg to ping server. 
	def senddata(self, msg):
		if msg:
			temp = json.dumps(msg).encode("base64")
			self.send(temp)
			self.recvdata() #Wait for ACK message

#	recvdata waits for the server to acknowledge
#	Should close connection if timeout
#	IMPLEMENT TIMEOUT CODE HERE. SHOULD CLOSE IF TIMED OUT
	def recvdata(self):
		data = self.recv(1024)
		while(len(data) == 0):
			data = self.recv(1024)
		if data:
			m_data = json.loads(data.decode("base64"))
			if(m_data == "OK"): print "Server ACK"
			else: return m_data
