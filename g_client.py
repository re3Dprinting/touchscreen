from socket import *
import json
import errno
import select
import time

host = "192.168.1.169" 
port = 63200

#	The g_client class inherits from the socket class
class g_client(socket):
	def __init__(self, data_obj):
		self.data = data_obj
		self.is_conn = False
		self.catch_except(self.connect_client)

#	Main exception handling wrapper function
	def catch_except(self,function, arg1 = ""):
		try:
			if arg1 != "": function(arg1)
			else: function()
		except Exception as e:
			#errno.EAGAIN= 11, errno.EWOULDBLOCK = 11 
			if e.args[0] == errno.EAGAIN or e.args[0] == errno.EWOULDBLOCK:
				#print "No Data from Server/ Server not responding"
				if not self.data.start_timeout_seq: 
					self.data.counter[2] = 0
					self.data.start_timeout_seq = True
				if self.data.server_timeout and self.is_conn:
					self.is_conn = False
					self.data.start_timeout_seq = False
					print "Server Timeout Out! Please reset."
			elif e.args[0] == 32 or e.args[0] == 104:
				self.is_conn = False
				print "Server Disconnected!"
			elif e.args[0] == 111:
				print "Error Connecting to Server: ", e
				self.data.server_timeout = False
				self.is_conn = False
			else:
				self.is_conn = False
				print "New error: ", e

#	Initial attempt to connect to server
#	Non-blocking program 
	def connect_client(self):
		if not self.is_conn:
			socket.__init__(self,AF_INET,SOCK_STREAM)
			self.setblocking(False)
			err = self.connect_ex((host,port))
			time.sleep(.08)
			err_no = self.getsockopt(SOL_SOCKET,SO_ERROR)
			# if err_no != 0: print err_no, errno.errorcode[err_no]
			# else: print err_no
			if err_no == 0: 
				self.is_conn = True
				self.data.addtobuffer("ST", self.data.status)
			if err_no == 111: 
				raise error(111, "Connection refused.")

		#if self.is_conn: self.data.addtobuffer("ST", self.data.status)

#	Attempt to reconnect to Server
	def attemptconnect(self, data):
		if not self.is_conn: self.__init__(data)

#	senddata function converts data into json string then encodes it
#	If no data, send "None" msg to ping server. 
	def senddata(self, msg):
		self.catch_except(self.send_d, msg)
	def send_d(self, msg):
		temp = json.dumps(msg).encode("base64")
		self.send(temp)
		self.recvdata() #Wait for ACK message

#	recvdata waits for the server to acknowledge
#	Non-blocking, raises errono 11 if no data is recieved
	def recvdata(self):
		data = self.recv(1024)
		if data:
			self.data.start_timeout_seq = False
			m_data = json.loads(data.decode("base64"))
			if(m_data == "OK"): print "Server ACK"
			else: return m_data

