from chromebookserver import *
from socket import *
from gigabotclient import *



class mainhandler():
	def __init__(self):
		self.server = socket(AF_INET, SOCK_STREAM) 
		self.server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) 
		self.server.bind((TCP_IP, TCP_PORT)) 
		self.server.listen(5)
		self.message = "Chromebook Gigabot Dashboard Data Server : \nWaiting for connections Gigabot clients..."
		self.gigabotthreads = []
		self.gigabots = []

#   check_dup function checks if there is already a present Gigabotnode,
#   with the same ipaddress. Returns that object if it is a match, otherwise, create a new instance. 
	def check_dup(self, ip):
		for bot in self.gigabots:
			if bot.ipaddress == ip:
				return bot
		new_g = gigabotclient(str(ip))
		self.gigabots.append(new_g)
		return new_g

	def listen_for_clients(self):
		(connection, (ip,port)) = self.server.accept()
		machine = self.check_dup(ip)
		newthread = GigabotThread(connection,ip,port, machine)
		newthread.start()
		self.gigabotthreads.append(newthread)

	def app_kill(self):
		for t in self.gigabotthreads:
			t.join()
		self.gigabots.clear()


# if __name__ == "__main__":
# 	man = mainhandler()
# 	print "Chromebook Gigabot Dashboard Data Server : \nWaiting for connections Gigabot clients..." 
# 	while(True):
# 		man.listen_for_clients()
# 	man.app_kill()
