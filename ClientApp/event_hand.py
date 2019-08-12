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

#		Setting up temperature Sets, and material preheats
		self.sete1temp = 0
		self.sete2temp = 0
		self.setbedtemp = 0

		self.m1 = Material(180,180,60,self)
		self.m2 = Material(215,215,115,self)
		self.m3 = Material(200,200,60,self)

		self.bedflash = 0
		self.sende1temp = False
		self.sende2temp = False
		self.sendbedtemp = False

	def run(self):
		while(True):
			time.sleep(0.5)
			self.tempwindow.updatetemperatures()
			self.sendperiphtemps()
			self.flashbedicon()
			if(not self.serial.is_open):
				self.reconnect_serial.emit("reconnectserial")



	def sete1(self, num):
		self.sete1temp = num
		self.tempwindow.changeText(self.tempwindow.e1set, str(self.sete1temp))
		self.sende1temp = True
	def sete2(self, num):
		self.sete2temp = num
		self.tempwindow.changeText(self.tempwindow.e2set, str(self.sete2temp))
		self.sende2temp = True
	def setb(self, num):
		self.setbedtemp = num
		self.tempwindow.changeText(self.tempwindow.bedset, str(self.setbedtemp))
		self.sendbedtemp = True
	def increment_e1(self):
		self.sete1temp +=1
		self.tempwindow.changeText(self.tempwindow.e1set, str(self.sete1temp))
		self.sende1temp = True
	def increment_e2(self):
		self.sete2temp +=1
		self.tempwindow.changeText(self.tempwindow.e2set, str(self.sete2temp))
		self.sende2temp = True
	def increment_bed(self):
		self.setbedtemp +=1
		self.tempwindow.changeText(self.tempwindow.bedset, str(self.setbedtemp))
		self.sendbedtemp = True
	def decrement_e1(self):
		if self.sete1temp > 0: self.sete1temp -=1
		self.tempwindow.changeText(self.tempwindow.e1set, str(self.sete1temp))
		self.sende1temp = True
	def decrement_e2(self):
		if self.sete2temp > 0: self.sete2temp -=1
		self.tempwindow.changeText(self.tempwindow.e2set, str(self.sete2temp))
		self.sende2temp = True
	def decrement_bed(self):
		if self.setbedtemp > 0: self.setbedtemp -=1
		self.tempwindow.changeText(self.tempwindow.bedset, str(self.setbedtemp))
		self.sendbedtemp = True


	def sendperiphtemps(self):
		if self.sende1temp:
			self.tempwindow.serial.send_serial('M104 T0 S'+str(self.sete1temp))
			self.sende1temp = False
		if self.sende2temp:
			self.tempwindow.serial.send_serial('M104 T1 S'+str(self.sete2temp))
			self.sende2temp = False
		if self.sendbedtemp:
			self.tempwindow.serial.send_serial('M140 S'+str(self.setbedtemp))
			self.sendbedtemp = False
	def flashbedicon(self):
		if self.setbedtemp >= 50:
			self.bedflash += 1
			if self.bedflash == 2:
			    self.tempwindow.bedimg.setIcon(self.tempwindow.unheated)
			elif self.bedflash == 4:
			    self.tempwindow.bedimg.setIcon(self.tempwindow.bedheated1)
			elif self.bedflash == 6:
			    self.tempwindow.bedimg.setIcon(self.tempwindow.bedheated2)
			    self.bedflash = 0
		else:
			self.tempwindow.bedimg.setIcon(self.tempwindow.unheated)
		