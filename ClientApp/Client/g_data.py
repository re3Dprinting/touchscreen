from socket import *
import time
import threading
from PyQt5 import QtCore
#	g_data class is derived from the Thread class for timing applicataions.
#	g_data class also handles parsing data and a buffer that is periodically sent to the server
class g_data(QtCore.QThread):
	checkserial_msg = QtCore.pyqtSignal([str],[unicode])
	checkserver_msg = QtCore.pyqtSignal([str],[unicode])
	updatefiles = QtCore.pyqtSignal([str],[unicode])
	printcancelled = QtCore.pyqtSignal([str],[unicode])
	updateprogress = QtCore.pyqtSignal([str],[unicode])
	printfinished = QtCore.pyqtSignal([str],[unicode])
	def __init__(self):
		super(g_data,self).__init__()
		self.counter = [0,0] # Serial Counter, Server Counter
		self.serial = None
		self.serial_msg = None
		self.client = None
		self.client_msg = None

#	Data to be extracted
		self.waittemp = False
		self.waitprogress = False
		self.temp = {'T0': [0,0], 'T1': [0,0], 'B': [0,0]}
		self.uploaddate= ""
		self.model = ""
		self.header = ""
		self.status = ""
		self.printtime = ""
		self.currentfile = ""
		self.progress = []
		self.files = dict()
		self.stats = dict()
		self.buffer = dict()
		self.ipaddr = self.getipaddress()
		self.position = {'X': 0, 'Y': 0, 'Z':0, 'E':0}
		self.homeposition = {'X': 508, 'Y': 0, 'Z':0}
		self.maxposition = {'X': 508, 'Y': 463, 'Z':600}
	def stop(self):
		self.start = False
#	Mainthread for timers
#	counter list consists of reconnflag/sendflag
	def run(self):
		while True:
			time.sleep(0.1)
			if self.serial.is_open:
			#Wait five seconds after connection:
			#- read initial header
			#- Send gcode to enable periodic temperature reading
				#print self.counter[0], " Reset? ",self.serial.just_open
				self.counter[0] += 1
				if self.serial.just_open:
					if self.counter[0] >= 100:
						self.serial.initserial()
						self.serial.just_open = False
						self.counter[0] = 0
				else:
					err = self.serial.readdata()
					if err != None:
						self.serial_msg = err
						self.checkserial_msg.emit("checkserial")
						self.printcancelled.emit("printcancelled")
					if not self.status == "AC" and not self.serial.just_open:
						if self.counter[0] >= 10:
							if not self.waittemp: self.serial.send_serial('M105')
							self.counter[0] = 0
					elif self.status == "AC" and not self.serial.just_open:
						if self.counter[0] >= 150:
							if not self.waitprogress: self.serial.send_serial("M27")
							self.counter[0] = 0

				# print self.counter[0]
				# if self.counter[0] >= 10:
				# 	if self.counter[0] >= 100:
				# 		self.serial.initserial()
				# 		self.counter[0] = 0

				# elif self.counter[0] < 10:
				# 	if self.counter[0] == 1:
				# 		err = self.serial.readdata()
				# 		if err != None:
				# 			self.serial_msg = err
				# 			self.checkserial_msg.emit("checkserial")
				# 			self.printcancelled.emit("printcancelled")
				# 	if self.counter[0] >= 2 and self.counter[0] < 10 :
				# 		if not self.waittemp and not self.status == "AC": self.serial.send_serial('M105')
				# 		if not self.waitprogress and self.status == "AC": self.serial.send_serial("M27")
				# 		self.counter[0] = 0

			if self.client.is_conn:
				if self.client.just_conn and self.serial.is_open:
					self.buffer.clear()
					self.addtobuffer("HD",self.header)
					self.addtobuffer("SS",self.stats)
					self.addtobuffer("ST",self.status)
					self.addtobuffer("FI", self.currentfile)
					self.client_msg = self.client.senddata()
					if self.client_msg != None:
						self.checkserver_msg.emit("checkserver_msg")
					self.client.just_conn = False
					self.buffer.clear()
				if self.counter[1] >= 50:
					self.client_msg = self.client.senddata()
					if self.client_msg != None:
						self.checkserver_msg.emit("checkserver_msg")
					self.buffer.clear()
					self.counter[1] = 0
				self.counter[1]+= 1

	def resettemps(self):
		self.temp = {'T0': [0,0], 'T1': [0,0], 'B': [0,0]}
	def resetsettemps(self):
		for t in self.temp: self.temp[t][1] = 0

#	Attempt to get the IP address through connecting to Google DNS to get current ipaddress
	def getipaddress(self):
		try:
			s = socket(AF_INET, SOCK_DGRAM)
			s.connect(("8.8.8.8",80))
			ip = s.getsockname()[0]
			s.close()
			return ip
		except error, exc:
			return ""

#	Add data to buffer to be sent through the SenderThread
	def addtobuffer(self, item, val):
		self.buffer[item] = val

#	Main Data Handling Function
	def parsedata(self, msglen, serialdata):
		data_ = serialdata.decode("utf-8")
		if ("busy:" in data_): 
			self.waittemp = True
			self.waitprogress = True
		else: 
			self.waitemp = False
			self.waitprogress = False
		if( "M23" in data_ and "M24" in data_):
			self.extractprintfile(data_)
			self.addtobuffer("FI", self.currentfile)
			time.sleep(4)
		if('T0' in data_):
			self.extracttemp("T0:", data_)
			self.extracttemp("T1:", data_)
			self.extracttemp("B:", data_)
			self.addtobuffer("T", self.temp)
			self.waittemp = False
			#self.check_printing()
		if(msglen >200 and "Updated" in data_):
			self.extractheader(data_)
			self.addtobuffer("HD", self.header)
		if("Stats:" in data_):
			self.extractstats(data_)
			self.addtobuffer("SS", self.stats)
		if("Count" in data_):
			self.extractposition(data_)
		if("Begin file" in data_ or "End file" in data_):
			self.extractfiles(data_)
			self.updatefiles.emit("updatefiles")
		if ("SD printing" in data_):
			self.extractprogress(data_)
			self.waitprogress = False

#	Check if Print was stopped
#	If printer's status is Idle, and there is a current file and the heaters are on, change to Active
#	If printer's status is Active, and there is a current file, and the heaters are off, change to Idle	
	# def check_printing(self):
	# 	idle = True
	# 	for t in self.temp:
	# 		if self.temp[t][1] != 0 : idle = False
	# 	if(self.status == "ON" and self.currentfile != "" and not idle):
	# 		self.changestatus("AC")
	# 	elif(self.status == "AC" and self.currentfile != "" and idle):
	# 		print "Print Cancelled!"
	# 		self.printcancelled.emit("printcancelled")
	# 		self.changestatus("ON")
	# 		self.currentfile = ""




#	Change the status of the printer
#	ON: Idle/Connected, OF: Off/Disconnected, AC: Active/Printing, UM: Under Maintanence  
	def changestatus(self, stat):
		if(self.status != stat):
			self.status = stat
			self.addtobuffer("ST", stat)

#	Done printing file
	def checkfinishprinting(self, data):
		data = data.split("\n")
		for d in data:
			if "Done printing file" in d:
				self.status = "ON"
				self.printfinished.emit("printfinished")

#	SD printing byte 6327/5335491
	def extractprogress(self, data):
		data = data.split("\n")
		for d in data:
			if "SD printing" in d:
				tmp = d.split(" ")[-1]
				tmp = tmp.split("/")
				if (tmp[0].isdigit() and tmp[1].isdigit()):
					self.progress = [int(tmp[0]), int(tmp[1])]
					self.updateprogress.emit("updateprogress")
				break



#	Begin file list
#	GUITAR~1.GCO 5335491
#	End file list
	def extractfiles(self,data):
		data_ = data.split('\n')
		for d in data_:
			if ".GCO" in d:
				tmp = d.split(" ")
				self.files[tmp[0]] = tmp[1]

#	Temperature Data Sample
#	T:140.69 /0.00' B:52.00 /0.00 T0:140.69 /0.00 T1:24.41 /0.00 @:0 B@:0 @0:0 @1:0
	def extracttemp(self,variable,data):
		#Extracting temperature data to a tuple in the format (Temp/SetTemp)
		if variable in data:
			start = end = data.rfind(variable) + len(variable)
			while(((ord(data[end]) < 58 and ord(data[end])>45) or ord(data[end]) == 32) and end<(len(data)-1)): end+=1
			temptup = data[start:end].split("/")
			if(len(temptup) > 1):
				tup = [float(x) for x in temptup]
				self.temp[variable[:-1]] = tup

#	X:508.00 Y:0.00 Z:5.00 E:0.00 Count X:60208 Y:0 Z:20158
	def extractposition(self, data):
		data_ = data.split("\n")
		tmp = ""
		for d in data_: 
			if "Count" in d: 
				tmp = d.split(" Count ")
				pos = tmp[0].split(" ")
				for ax in pos:
					temp = ax.split(":")
					self.position[temp[0]] = float(temp[1])
				break

#	Header Data Sample
#	start
#	echo:Marlin bugfix-2.0.x
#	echo: Last Updated: Jun 12 2019 13:30:34 | Author: (GB3, V4.x.x)
#	echo:Compiled: Jun 12 2019
#	echo: Free Memory: 1201  PlannerBufferBytes: 2784
	def extractheader(self, data):
		#Searching for last updated timestamp
		start = end = data.find("Last Updated:") + len("Last Updated:")
		while(ord(data[end]) != 124): end += 1
		self.uploaddate = data[start:end].strip()
		start = end
		#Increment until you hit "G" for GB
		while(ord(data[start]) != 66): start += 1
		end = start
		while(ord(data[end]) != 86): end += 1
		modstring = data[start+1:end].strip()
		self.model = "Regular" if "3" in modstring else modstring
		self.header = self.uploaddate + ".." + self.model
#	Print File Sample
#	echo:enqueueing "M23 thumbp~1.gco"
#	echo:enqueueing "M24"
#	echo:Now fresh file: thumbp~1.gco
	def extractprintfile(self,data_):
		start = end = data_.find(".gco") + len(".gco")
		while(ord(data_[start]) != 32): start-=1
		self.currentfile = data_[start:end]

#	Stat Data Sample
#	Stats: Prints: 28, Finished: 26, Failed: 2
#	Stats: Total time: 11d 21h 42m 59s, Longest job: 5d 12h 41m 17s
#	Stats: Filament used: 628.09m
	def extractstats(self, data_):
		d_list = data_.split("\n")
		for i in range(len(d_list)):
			if "Stat" in d_list[i]:
				d_list[i] = d_list[i].strip("Stats: ").split(",")
				for j in range(len(d_list[i])):
					data_component = d_list[i][j].split(":")
					self.stats[data_component[0].strip()] = data_component[1].strip()

# x = "X:508.00 Y:0.00 Z:5.00 E:0.00 Count X:60208 Y:0 Z:20158"
# dataclass = g_data()
# dataclass.extractposition(x)