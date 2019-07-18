from socket import *
import time

class g_data:
	def __init__(self):
		self.temp = dict()
		self.uploaddate= ""
		self.model = ""
		self.status = ""
		self.printtime = ""
		self.currentfile = ""
		self.stats = dict()
		self.buffer = dict()
		s = socket(AF_INET, SOCK_DGRAM)
		s.connect(("8.8.8.8",80))
		self.ipaddr = s.getsockname()[0]
		s.close()

	def changestatus(self, stat):
		self.status = stat
		self.buffer["ST"] = stat

	def addtobuffer(self, item, val):
		self.buffer[item] = val

	def extracttemp(self,variable,data):
		#Extracting temperature data to a tuple in the format (Temp/SetTemp)
		if variable in data:
			start = end = data.rfind(variable) + len(variable)
			while(((ord(data[end]) < 58 and ord(data[end])>45) or ord(data[end]) == 32) and end<(len(data)-1)): end+=1
			temptup = data[start:end].split("/")
			if(len(temptup) > 1):
				tup = [float(x) for x in temptup]
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
	
	def extractprintfile(self,data_):
		start = end = data_.find(".gco") + len(".gco")
		while(ord(data_[start]) != 32): start-=1
		self.currentfile = data_[start:end]

#  Sample Stat Data Line from Serial Read
#  Stats: Prints: 28, Finished: 26, Failed: 2
#  Stats: Total time: 11d 21h 42m 59s, Longest job: 5d 12h 41m 17s
#  Stats: Filament used: 628.09m
	def extractstats(self, data_):
		d_list = data_.split("\n")
		for i in range(len(d_list)):
			d_list[i] = d_list[i].strip("Stats: ").split(",")
			for j in range(len(d_list[i])):
				data_component = d_list[i][j].split(":")
				self.stats[data_component[0].strip()] = data_component[1].strip()

	def check_printing(self):
		idle = True
		for t in self.temp:
			if self.temp[t][1] != 0 : idle = False
		if(self.status == "ON" and self.currentfile != "" and not idle):
			self.changestatus("AC")
		elif(self.status == "AC" and self.currentfile != "" and idle):
			self.changestatus("ON")
			self.currentfile = ""

	def parsedata(self, msglen, data):
		data_ = data.decode("utf-8")
		if( "M23" in data_ and "M24" in data_):
			self.extractprintfile(data_)
			self.buffer["FI"] = self.currentfile
			time.sleep(4)
		if(msglen <200 and 'T0' in data_):
			self.extracttemp("T0:", data_)
			self.extracttemp("T1:", data_)
			self.extracttemp("B:", data_)
			self.buffer["T"] = self.temp
			self.check_printing()
			return self.temp
		if(msglen >200 and "Updated" in data_):
			self.extractheader(data_)
			self.buffer["HD"] = self.uploaddate + ".." + self.model
			return self.uploaddate + ".." + self.model
		if("Stats:" in data_):
			self.extractstats(data_)
			self.buffer["SS"] = self.stats
			return self.stats
