from socket import *

class g_data:
	def __init__(self):
		self.temp = dict()
		self.uploaddate= ""
		self.model = ""
		self.status = ""
		self.printtime = ""
		s = socket(AF_INET, SOCK_DGRAM)
		s.connect(("8.8.8.8",80))
		self.ipaddr = s.getsockname()[0]
		s.close()

	def extracttemp(self,variable,data):
		#Extracting temperature data to a tuple in the format (Temp/SetTemp)
		if variable in data:
			start = end = data.find(variable) + len(variable)
			while((ord(data[end]) < 58 and ord(data[end])>45) or ord(data[end]) == 32): end+=1
			tup = [float(x) for x in data[start:end].split("/")]
			self.temp[variable[:-1]] = tup
	def extractheader(self, data):
		#Searching for last updated timestamp
		start = end = data.find("Last Updated:") + len("Last Updated:")
		while(ord(data[end]) != 124): end += 1
		self.uploaddate = data[start:end].strip()
		#print self.uploaddate
		start = end
		#Increment until you hit "G" for GB
		while(ord(data[start]) != 66): start += 1
		end = start
		while(ord(data[end]) != 86): end += 1
		modstring = data[start+1:end].strip()
		self.model = "Regular" if "3" in modstring else modstring

	def parsedata(self, len, d):
		msglen = len
		data = d
		data = data.decode("utf-8")
		if(msglen <200 and 'T' in data):
			self.extracttemp("T0:", data)
			self.extracttemp("T1:", data)
			self.extracttemp("B:", data)
			return self.temp
		if(msglen >200 and "Updated" in data):
			self.extractheader(data)
			return self.uploaddate + ".." + self.model
