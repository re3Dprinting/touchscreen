import time
import threading
from preheatmaterial import *
from PyQt5 import QtCore


# The Event Handler operates the temperature preheats, setting the temperatures, 
# 

class event_handler(QtCore.QThread):
	reconnect_serial = QtCore.pyqtSignal([str],[unicode])
	def __init__(self, serial, tempwindow = None, serialwindow = None):
		super(event_handler,self).__init__()
		self.tempwindow = tempwindow
		self.serialwindow = serialwindow
		self.serial = serial

		self.feedrate = 100
		self.fr_index = 0
		self.flowrate = [100, 100, 100]
		self.fr_text = ["All", "E1", "E2"]
		self.babystep = 0
		self.babystepx10 = 0
		self.babystepinc = 1


#		Setting up temperature Sets, and material preheats
		self.sete1temp = 0
		self.sete2temp = 0
		self.setbedtemp = 0
		self.m1 = Material(180,180,60,self)
		self.m2 = Material(215,215,115,self)
		self.m3 = Material(200,200,60,self)
		self.sendtempcount = 0

		self.bedflash = 0


	def run(self):
		while(True):
			time.sleep(0.1)
			self.sendtempcount += 1
			if self.sendtempcount >= 30: 
				self.tempwindow.updatesettemperatures()
				self.sendtempcount = 0
			self.tempwindow.updatetemperatures()
			self.flashbedicon()
			if(not self.serial.is_open):
				self.reconnect_serial.emit("reconnectserial")

	def resetparameters(self):
		self.feedrate = 100
		self.flowrate = [100, 100, 100]
		self.babystep = float(0)

	def sendbabystep(self):
		self.tempwindow.serial.send_serial("M290 Z "+ str(self.babystep))

	def sendflowrate(self):
		if self.fr_index == 0: 
			self.tempwindow.serial.send_serial("M221 S" + str(self.flowrate[self.fr_index]) + " T0")
			self.tempwindow.serial.send_serial("M221 S" + str(self.flowrate[self.fr_index]) + " T1")
			self.flowrate[1] = self.flowrate[2] = self.flowrate[0]
		else:
			if self.fr_index == 1: t = " T0"
			else: t = " T1"
			self.tempwindow.serial.send_serial("M221 S" + str(self.flowrate[self.fr_index]) + t)

#Used for preheating temperatures
	def sete1(self, num):
		self.sete1temp = num
		self.tempwindow.changeText(self.tempwindow.e1set, str(self.sete1temp))
		self.sendperiphtemps("e1")
	def sete2(self, num):
		self.sete2temp = num
		self.tempwindow.changeText(self.tempwindow.e2set, str(self.sete2temp))
		self.sendperiphtemps("e2")
	def setb(self, num):
		self.setbedtemp = num
		self.tempwindow.changeText(self.tempwindow.bedset, str(self.setbedtemp))
		self.sendperiphtemps("bed")

#	Incrementing temperature through the non-printing menu.
	def increment_e1(self):
		self.sete1temp +=1
		self.tempwindow.changeText(self.tempwindow.e1set, str(self.sete1temp))
		# self.tempwindow.changeText(self.tempwindow.e1set, str(int(self.serial.data.temp["T0"][1])))
		self.sendperiphtemps("e1")
	def increment_e2(self):
		self.sete2temp +=1
		self.tempwindow.changeText(self.tempwindow.e2set, str(self.sete2temp))
		# self.tempwindow.changeText(self.tempwindow.e2set, str(int(self.serial.data.temp["T1"][1])))
		self.sendperiphtemps("e2")
	def increment_bed(self):
		self.setbedtemp +=1
		self.tempwindow.changeText(self.tempwindow.bedset, str(self.setbedtemp))
		# self.tempwindow.changeText(self.tempwindow.bedset, str(int(self.serial.data.temp["B"][1])))
		self.sendperiphtemps("bed")
	def decrement_e1(self):
		if self.sete1temp > 0: self.sete1temp -=1
		self.tempwindow.changeText(self.tempwindow.e1set, str(self.sete1temp))
		# self.tempwindow.changeText(self.tempwindow.e1set, str(int(self.serial.data.temp["T0"][1])))
		self.sendperiphtemps("e1")
	def decrement_e2(self):
		if self.sete2temp > 0: self.sete2temp -=1
		self.tempwindow.changeText(self.tempwindow.e2set, str(self.sete2temp))
		# self.tempwindow.changeText(self.tempwindow.e2set, str(int(self.serial.data.temp["T1"][1])))
		self.sendperiphtemps("e2")
	def decrement_bed(self):
		if self.setbedtemp > 0: self.setbedtemp -=1
		self.tempwindow.changeText(self.tempwindow.bedset, str(self.setbedtemp))
		# self.tempwindow.changeText(self.tempwindow.bedset, str(int(self.serial.data.temp["B"][1])))
		self.sendperiphtemps("bed")


	def sendperiphtemps(self, periph):
		if periph == "e1": self.tempwindow.serial.send_serial('M104 T0 S'+str(self.sete1temp))
		elif periph == "e2": self.tempwindow.serial.send_serial('M104 T1 S'+str(self.sete2temp))
		elif periph == "bed": self.tempwindow.serial.send_serial('M140 S'+str(self.setbedtemp))
		self.sendtempcount = 0

	def flashbedicon(self):
		if self.setbedtemp >= 50:
			self.bedflash += 1
			if self.bedflash == 6:
			    self.tempwindow.bedimg.setIcon(self.tempwindow.unheated)
			elif self.bedflash == 12:
			    self.tempwindow.bedimg.setIcon(self.tempwindow.bedheated1)
			elif self.bedflash == 18:
			    self.tempwindow.bedimg.setIcon(self.tempwindow.bedheated2)
			    self.bedflash = 0
		else:
			self.tempwindow.bedimg.setIcon(self.tempwindow.unheated)
		