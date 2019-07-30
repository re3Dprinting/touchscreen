
#	gigabotclient instance is created whenever a new client is connected. 
#	The object is reused if the IP address matches the IP of the connected device
class gigabotclient():
	def __init__(self, ipaddress):
		self.idnum = "999"
		self.model = "default"
		self.ipaddress = ipaddress
		self.status = "OF"
		self.btemp = (0,0)
		self.temp1 = (0,0)
		self.temp2 = (0,0)
		self.currentfile = ""
		self.dateuploaded = ""
		self.modulelinked = False
		self.module = None
		self.moduleshow = False
	def updatetemp(self, newtemp):
		self.btemp = newtemp[0]
		self.temp1 = newtemp [1]
		self.temp2 = newtemp [2]
	def updateprinttime(self, newprint):
		self.printtime += newprint

	def getdata(self):
		return "Gigabot #",self.idnum," \n" + self.model + "\n" + "Last Updated: \t" + self.dateuploaded + "\n" + "IP address:\t" + self.ipaddress + "\n"
#	OF- Off/Disconnected ON- On/Idle UM- Under Maintenence AC- Active/Printing
	def getstatus(self):
	 	if(self.status == "ON"): return "Idle/Connected\n"
	 	elif(self.status == "OF"): return "Off/Disconnected\n"
	 	elif(self.status == "AC"): return "Active/Printing\n"
	def getstats(self):
		for key in self.stats:
			return key, ":\t", self.stats[key]
	def gettemp1(self): 
		return str(self.temp1[0])+ " / "+ str(self.temp1[1])
	def gettemp2(self): 
		return str(self.temp2[0])+ " / "+ str(self.temp2[1])
	def getbtemp(self): 
		return str(self.btemp[0])+ " / "+ str(self.btemp[1])

	def printdata(self):
		print "Gigabot #",self.idnum," \n" + self.model + "\n" + "Last Updated: \t" + self.dateuploaded + "\n" + "IP address:\t" + self.ipaddress + "\n"
#	OF- Off/Disconnected ON- On/Idle UM- Under Maintenence AC- Active/Printing
	def printstatus(self):
	 	if(self.status == "ON"): print "STATUS: Gigabot is Idle/Connected\n"
	 	elif(self.status == "OF"): print "STATUS: Gigabot is Off/Disconnected\n"
	 	elif(self.status == "AC"): print "STATUS: Gigabot is Active/Printing\n"
	def printstats(self):
		for key in self.stats:
			print key, ":\t", self.stats[key]
	def printtemp(self): 
		print "T1:\t" + str(self.temp1[0]) + "/" + str(self.temp1[1]) + "\t" + "T2:\t" + str(self.temp2[0]) + "/" + str(self.temp2[1]) + "\t" + "B:\t" + str(self.btemp[0]) + "/" +str(self.btemp[1]) 
	def parsedata(self, d_ata):
		print d_ata
		if ("ST" in d_ata):
			self.status = d_ata["ST"]
			print self.printstatus()
		if ("T" in d_ata):
			self.btemp = d_ata["T"]["B"]
			self.temp1 = d_ata["T"]["T0"]
			self.temp2 = d_ata["T"]["T1"]
			print self.printtemp()
		if("FI" in d_ata):
			self.currentfile = d_ata["FI"]
			print "Current File: " + self.currentfile + "\n"
		if ("HD" in d_ata):
			m = d_ata["HD"].split("..")
			self.dateuploaded = m[0]
			self.model = m[1]
			self.printdata()
		if("SS" in d_ata):
			self.stats = d_ata["SS"]
			self.printstats()
	
