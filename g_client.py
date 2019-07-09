from socket import *
import json

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
