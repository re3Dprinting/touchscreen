import time
import threading
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

		self.sendtempcount = 0

		self.bedflash = 0


	def run(self):
		while(True):
			time.sleep(0.1)
			self.sendtempcount += 1
			if self.sendtempcount >= 40: 
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


	def flashbedicon(self):
		if self.tempwindow.heatedbed.settemp >= 50:
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
		