from socket import *
import json
import errno
import select
import time
import os

host = "192.168.1.49" 
port = 63200

#	The g_client class inherits from the socket class
class g_client(socket):
	def __init__(self, data_obj):
		self.data = data_obj
		self.data.client = self
		self.host = "192.168.1.49"
		self.port = 63200
		self.just_conn = False
		self.is_conn = False
		
#	Main exception handling wrapper function
	def catch_except(self,function, arg1 = ""):
		try:
			if arg1 != "": return function(arg1)
			else: return function()
		except Exception as e:
#			Exception for handling server timeout
			if e.args[0] == errno.EAGAIN or e.args[0] == errno.EWOULDBLOCK:
				return "Server Timeout Out! Please reset." + str(e)
			elif e.args[0] == 32 or e.args[0] == 104:
				self.is_conn = False
				# self.data.server_timeout = False
				return "Server Disconnected!" + str(e)
			elif e.args[0] == 111:
				# self.data.server_timeout = False
				self.is_conn = False
				return "Error Connecting to Server: " + str(e)
			else:
				self.is_conn = False
				return "New error: " + str(e)

#	Initial attempt to connect to server
#	Non-blocking program using connect_ex and getsockopt to catch errors
	def attemptconnect(self):
		if not self.is_conn: 
			return self.catch_except(self.conn_client)
		
	def conn_client(self):
		if not self.is_conn:
			socket.__init__(self,AF_INET,SOCK_STREAM)
			err = self.connect_ex((host,port))
			self.setblocking(False)
			err_no = self.getsockopt(SOL_SOCKET,SO_ERROR)
			if(err == 0 and err_no == 0):
				return "Connected to Server"
				self.just_conn = True
				self.is_conn = True
			else:
				if err != 0: raise error(err, os.strerror(err))
				if err_no != 0: raise error( err_no, os.strerror(err_no))

#	senddata function converts data into json string then encodes it
#	If no data, send "None" msg to ping server. 
	def senddata(self):
		return self.catch_except(self.send_d, self.data.buffer)

	def send_d(self, msg):
		temp = json.dumps(msg).encode("base64")
		rd, wt, er = select.select([self],[self],[self])
		if wt:
			self.send(temp)
		if rd: 
			# start timeout sequence
			self.recvdata()

#	recvdata waits for the server to acknowledge
#	Non-blocking, raises errono 11 if no data is recieved
	def recvdata(self):
		data = self.recv(1024)
		if data:
			self.data.start_timeout_seq = False
			m_data = json.loads(data.decode("base64"))
			if(m_data == "OK"): print "Server ACK"
			else: return m_data

