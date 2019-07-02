
class gigabotclient():
	def __init__(self, idnum, model, ipaddress, status):
		self.idnum = idnum
		self.model = model
		self.ipaddress = ipaddress
		self.status = status
		self.btemp = (0,0)
		self.temp1 = (0,0)
		self.temp2 = (0,0)
		self.printtime = 0
		self.dateuploaded = ""
	def updatetemp(self, newtemp):
		self.btemp = newtemp[0]
		self.temp1 = newtemp [1]
		self.temp2 = newtemp [2]
	def updateprinttime(self, newprint):
		self.printtime += newprint
	def printdata(self):
		print "Gigabot #",self.idnum," " + self.model + "\n"
		print "Last Updated: " + self.dateuploaded + "\n"
		print "IP address:\t" + self.ipaddress + "\n"
		print "Total Print Time:\t", self.printtime, "\n"
	def parsedata(self, d_ata):
		if ("B" in d_ata):
			self.btemp = d_ata["B"]
			self.temp1 = d_ata["T0"]
			self.temp2 = d_ata["T1"]
	def printtemp(self): 
		print "T1:\t" + str(self.temp1[0]) + "/" + str(self.temp1[1]) + "\t" + "T2:\t" + str(self.temp2[0]) + "/" + str(self.temp2[1]) + "\t" + "B:\t" + str(self.btemp[0]) + "/" +str(self.btemp[1]) 

