
#	gigabotclient instance is created whenever a new client is connected. 
#	The object is reused if the IP address matches the IP of the connected device
class gigabotclient():
	def __init__(self, ipaddress):
		self.idnum = 999
		self.model = "default"
		self.ipaddress = ipaddress
		self.status = "OF"
		self.btemp = (0,0)
		self.temp1 = (0,0)
		self.temp2 = (0,0)
		self.currentfile = ""
		self.dateuploaded = ""
	def updatetemp(self, newtemp):
		self.btemp = newtemp[0]
		self.temp1 = newtemp [1]
		self.temp2 = newtemp [2]
	def updateprinttime(self, newprint):
		self.printtime += newprint
	def printdata(self):
		print "Gigabot #",self.idnum," " + self.model
		print "Last Updated: \t" + self.dateuploaded
		print "IP address:\t" + self.ipaddress + "\n"
#	OF- Off/Disconnected ON- On/Idle UM- Under Maintenence AC- Active/Printing
	def printstatus(self):
	 	if(self.status == "ON"): print "STATUS: Gigabot is Idle/Connected"
	 	elif(self.status == "OF"): print "STATUS: Gigabot is Off/Disconnected"
	 	elif(self.status == "AC"): print "STATUS: Gigabot is Active/Printing"
	def printstats(self):
		for key in self.stats:
			print key, ":\t", self.stats[key]
	def printtemp(self): 
		print "T1:\t" + str(self.temp1[0]) + "/" + str(self.temp1[1]) + "\t" + "T2:\t" + str(self.temp2[0]) + "/" + str(self.temp2[1]) + "\t" + "B:\t" + str(self.btemp[0]) + "/" +str(self.btemp[1]) 
	def parsedata(self, d_ata):
		if ("ST" in d_ata):
			self.status = d_ata["ST"]
			self.printstatus()
		if ("T" in d_ata):
			self.btemp = d_ata["T"]["B"]
			self.temp1 = d_ata["T"]["T0"]
			self.temp2 = d_ata["T"]["T1"]
			self.printtemp()
		if("FI" in d_ata):
			self.currentfile = d_ata["FI"]
			print "Current File: " + self.currentfile
		if ("HD" in d_ata):
			m = d_ata["HD"].split("..")
			self.dateuploaded = m[0]
			self.model = m[1]
			self.printdata()
		if("SS" in d_ata):
			self.stats = d_ata["SS"]
			self.printstats()
