from chromebookserver import *
from socket import *
from gigabotclient import *

TCP_IP = '' 
TCP_PORT = 63200
#	Serverhandler class that manages the start/stop of the server. 
#	The server also prevents duplicate devices from getting produced by checking ip addresses
class serverhandler():
	def __init__(self):
		self.gigabotthreads = []
		self.gigabots = []
		self.server = socket(AF_INET, SOCK_STREAM) 

#	Called by the server thread, when the startserver button is clicked
	def startserver(self):
		self.server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) 
		self.server.bind((TCP_IP, TCP_PORT)) 
		self.server.listen(5)
		#self.message = "Chromebook Gigabot Dashboard Data Server : \nWaiting for connections Gigabot clients..."
		return True
#	Called by the server thread, to shut down the server
	def stopserver(self):
		for t in self.gigabotthreads:
			t.join()
		del self.gigabotthreads[:]
		self.server.close()
		return True

	def check_dup_thread(self,conn,ip,port):
		for t in self.gigabotthreads:
			if t.ipaddress == ip:
				t.conn = conn
				print "Device with IP: " + ip, " reconnected"
				return (t, False)
		newgigabot = gigabotclient(ip)
		newthread = GigabotThread(conn,ip,port, newgigabot)
		self.gigabotthreads.append(newthread)
		self.gigabots.append(newgigabot)
		return (newthread, True)
#	Blocking function that waits for a client to accept connect.
	def listen_for_clients(self):
		(connection, (ip,port)) = self.server.accept()
#		Check if there exists a thread that was a stopped because of a connection.
		(thread, isnewthread) = self.check_dup_thread(connection,ip,port)
		if isnewthread: thread.start()
		else: thread.connected = True
		# for t in self.gigabotthreads:
		# 	if not t.isAlive():
		# 		self.gigabotthreads.remove(t)


#   check_dup function checks if there is already a present Gigabotnode,
#   with the same ipaddress. Returns that object if it is a match, otherwise, create a new instance. 
	# def check_dup_gigabot(self, ip):
	# 	for g in self.gigabots:
	# 		if g.ipaddress == ip:
	# 			return g
	# 	new_g = gigabotclient(str(ip))
	# 	self.gigabots.append(new_g)
	# 	return new_g
