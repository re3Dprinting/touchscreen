import time
import threading
from preheatmaterial import *
from PyQt5 import QtCore

class temphandler(QtCore.QThread):
	def __init__(self, serial, parent = None):
		super(temphandler,self).__init__()
		self.parent = parent
		self.serial = serial

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

	def sete1(self, num):
		self.sete1temp = num
		self.parent.changeText(self.parent.e1set, str(self.sete1temp))
		self.sende1temp = True
	def sete2(self, num):
		self.sete2temp = num
		self.parent.changeText(self.parent.e2set, str(self.sete2temp))
		self.sende2temp = True
	def setb(self, num):
		self.setbedtemp = num
		self.parent.changeText(self.parent.bedset, str(self.setbedtemp))
		self.sendbedtemp = True
	def increment_e1(self):
		self.sete1temp +=1
		self.parent.changeText(self.parent.e1set, str(self.sete1temp))
		self.sende1temp = True
	def increment_e2(self):
		self.sete2temp +=1
		self.parent.changeText(self.parent.e2set, str(self.sete2temp))
		self.sende2temp = True
	def increment_bed(self):
		self.setbedtemp +=1
		self.parent.changeText(self.parent.bedset, str(self.setbedtemp))
		self.sendbedtemp = True
	def decrement_e1(self):
		if self.sete1temp > 0: self.sete1temp -=1
		self.parent.changeText(self.parent.e1set, str(self.sete1temp))
		self.sende1temp = True
	def decrement_e2(self):
		if self.sete2temp > 0: self.sete2temp -=1
		self.parent.changeText(self.parent.e2set, str(self.sete2temp))
		self.sende2temp = True
	def decrement_bed(self):
		if self.setbedtemp > 0: self.setbedtemp -=1
		self.parent.changeText(self.parent.bedset, str(self.setbedtemp))
		self.sendbedtemp = True


	def run(self):
		while(True):
			time.sleep(0.5)
			self.parent.updatetemperatures()
			self.sendperiphtemps()
			self.flashbedicon()


	def sendperiphtemps(self):
		if self.sende1temp:
			self.parent.serial.send_serial('M104 T0 S'+str(self.sete1temp))
			self.sende1temp = False
		if self.sende2temp:
			self.parent.serial.send_serial('M104 T1 S'+str(self.sete2temp))
			self.sende2temp = False
		if self.sendbedtemp:
			self.parent.serial.send_serial('M140 S'+str(self.setbedtemp))
			self.sendbedtemp = False
	def flashbedicon(self):
		if self.setbedtemp >= 50:
			self.bedflash += 1
			if self.bedflash == 2:
			    self.parent.bedimg.setIcon(self.parent.unheated)
			elif self.bedflash == 4:
			    self.parent.bedimg.setIcon(self.parent.bedheated1)
			elif self.bedflash == 6:
			    self.parent.bedimg.setIcon(self.parent.bedheated2)
			    self.bedflash = 0
		else:
			self.parent.bedimg.setIcon(self.parent.unheated)
		