from socket import *
import time
import serial
import serial.tools.list_ports

class serialdata:
	def __init__(self):
		self.temp = dict()
		self.uploaddate= ""
		self.model = ""

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
		print(self.uploaddate)
		start = end
		#Increment until you hit "G" for GB
		while(ord(data[start]) != 66): start += 1
		end = start
		while(ord(data[end]) != 86): end += 1
		modstring = data[start+1:end].strip()
		if("3" in modstring): self.model = "Regular"
		else: self.model = modstring
		print self.model


	def parsedata(self,msglen, data):
		if(msglen <200 and 'T' in data):
			self.extracttemp("T0:", data)
			self.extracttemp("T1:", data)
			self.extracttemp("B:", data)
		if(msglen >200 and "Updated" in data):
			self.extractheader(data)


# if __name__ == "__main__":
# 	x = gigabotconnection()
# 	data = b' T:178.41 /180.00 B:59.39 /60.00 T0:178.41 /180.00 T1:26.31 /0.00 @:92 B@:127 @0:92 @1:0\n'
# 	decode = data.decode('utf-8')
# 	print(decode)
# 	x.parsedata(decode)
# 	print(x.temp)


