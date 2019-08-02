from socket import *
import time
import threading

#	g_data class is derived from the Thread class for timing applicataions.
#	g_data class also handles parsing data and a buffer that is periodically sent to the server
class g_data(threading.Thread):
	def __init__(self):
		super(g_data,self).__init__()
		self.counter = [0,0] # Reconnectflag, SendFlag, ServerTimeout
		self.reconnflag = False
		self.sendflag = False
		self._stop = False

#	Flags to determine if server timeout occured
		self.start_timeout_seq = False
		self.server_timeout = False

#	Data to be extracted
		self.temp = dict()
		self.uploaddate= ""
		self.model = ""
		self.header = ""
		self.status = ""
		self.printtime = ""
		self.currentfile = ""
		self.stats = dict()
		self.buffer = dict()
		self.ipaddr = self.getipaddress()

	def stop(self):
		self._stop = True
#	Mainthread for timers
#	counter list consists of [reconnflag/sendflag, servertimeoutflag]
	def run(self):
		while self._stop == False:
			if self.start_timeout_seq and not self.server_timeout:
				self.counter[1]+=1
			if not self.start_timeout_seq: 
				self.counter[0] +=1
			
			time.sleep(1)
			#print self.counter
			if self.counter[0] >= 5 and not self.start_timeout_seq:
				self.reconnflag = True
				self.sendflag = True
				self.counter[0] = 0

			if self.start_timeout_seq and not self.server_timeout:
				if self.counter[1] > 2: self.sendflag= True
				print "Time since last response: ", self.counter[1]
				if self.counter[1] >= 10:
					self.counter[1] = 0
					self.server_timeout = True
					self.start_timeout_seq = False

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
		if( "M23" in data_ and "M24" in data_):
			self.extractprintfile(data_)
			self.addtobuffer("FI", self.currentfile)
			time.sleep(4)
		if(msglen <200 and 'T0' in data_):
			self.extracttemp("T0:", data_)
			self.extracttemp("T1:", data_)
			self.extracttemp("B:", data_)
			self.addtobuffer("T", self.temp)
			self.check_printing()
		if(msglen >200 and "Updated" in data_):
			self.extractheader(data_)
			self.addtobuffer("HD", self.header)
		if("Stats:" in data_):
			self.extractstats(data_)
			self.addtobuffer("SS", self.stats)

#	Check if Print was stopped
#	If printer's status is Idle, and there is a current file and the heaters are on, change to Active
#	If printer's status is Active, and there is a current file, and the heaters are off, change to Idle
	def check_printing(self):
		idle = True
		for t in self.temp:
			if self.temp[t][1] != 0 : idle = False
		if(self.status == "ON" and self.currentfile != "" and not idle):
			self.changestatus("AC")
		elif(self.status == "AC" and self.currentfile != "" and idle):
			print "Print Cancelled!"
			self.changestatus("ON")
			self.currentfile = ""

#	Change the status of the printer
#	ON: Idle/Connected, OF: Off/Disconnected, AC: Active/Printing, UM: Under Maintanence  
	def changestatus(self, stat):
		if(self.status != stat):
			self.status = stat
			self.addtobuffer("ST", stat)

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