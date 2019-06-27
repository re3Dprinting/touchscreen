
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
		print "IP address:\t" + self.ipaddress + "\n"
		print "Bed Temp:\t", self.btemp, "\n"
		print "Temperature 1:\t", self.temp1, "\n"
		print "Temperature 2:\t", self.temp2, "\n"
		print "Total Time:\t", self.printtime, "\n"
