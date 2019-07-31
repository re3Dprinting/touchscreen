from chromebookserver import *
from socket import *
from gigabotclient import *


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
#   check_dup function checks if there is already a present Gigabotnode,
#   with the same ipaddress. Returns that object if it is a match, otherwise, create a new instance. 
	def check_dup(self, ip):
		for bot in self.gigabots:
			if bot.ipaddress == ip:
				return bot
		new_g = gigabotclient(str(ip))
		self.gigabots.append(new_g)
		return new_g
#	Blocking function that waits for a client to accept connect.
	def listen_for_clients(self):
		(connection, (ip,port)) = self.server.accept()
		machine = self.check_dup(ip)
		newthread = GigabotThread(connection,ip,port, machine)
		newthread.start()
		self.gigabotthreads.append(newthread)
		for t in self.gigabotthreads:
			if not t.isAlive():
				self.gigabotthreads.remove(t)

