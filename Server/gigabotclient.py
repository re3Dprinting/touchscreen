
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
		return "Gigabot #",self.idnum," " + self.model + "\n" + "Last Updated: \t" + self.dateuploaded + "\n" + "IP address:\t" + self.ipaddress + "\n"
#	OF- Off/Disconnected ON- On/Idle UM- Under Maintenence AC- Active/Printing
	def printstatus(self):
	 	if(self.status == "ON"): return "STATUS: Gigabot is Idle/Connected"
	 	elif(self.status == "OF"): return "STATUS: Gigabot is Off/Disconnected"
	 	elif(self.status == "AC"): return "STATUS: Gigabot is Active/Printing"
	def printstats(self):
		st = ""
		for key in self.stats:
			st += key, ":\t", self.stats[key], "\n"
		return st
	def printtemp(self): 
		return "T1:\t" + str(self.temp1[0]) + "/" + str(self.temp1[1]) + "\t" + "T2:\t" + str(self.temp2[0]) + "/" + str(self.temp2[1]) + "\t" + "B:\t" + str(self.btemp[0]) + "/" +str(self.btemp[1]) 
	def parsedata(self, d_ata):
		ret_data = ""
		if ("ST" in d_ata):
			self.status = d_ata["ST"]
			ret_data+= self.printstatus()
		if ("T" in d_ata):
			self.btemp = d_ata["T"]["B"]
			self.temp1 = d_ata["T"]["T0"]
			self.temp2 = d_ata["T"]["T1"]
			ret_data+= self.printtemp()
		if("FI" in d_ata):
			self.currentfile = d_ata["FI"]
			ret_data+= "Current File: " + self.currentfile + "\n"
		if ("HD" in d_ata):
			m = d_ata["HD"].split("..")
			self.dateuploaded = m[0]
			self.model = m[1]
			ret_data+= self.printdata()
		if("SS" in d_ata):
			self.stats = d_ata["SS"]
			ret_data+= self.printstats()
		return ret_data
