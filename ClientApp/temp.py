import time
import threading
from preheatmaterial import *


class temphandler(threading.Thread):
	def __init__(self, serial, parent = None):
		super(temphandler,self).__init__()
		self.parent = parent
		self.serial = serial

		self.setextruder1 = 0
		self.setextruder2 = 0
		self.setbed = 0


		self.m1 = Material(180,180,60,self)
		self.m2 = Material(215,215,115,self)
		self.m3 = Material(200,200,60,self)

		self.count = 0
		self.set = False


	def sete1(self, num):
		self.setextruder1 = num
		self.parent.changeText(self.parent.e1set, str(self.setextruder1))
		self.set = True
	def sete2(self, num):
		self.setextruder2 = num
		self.parent.changeText(self.parent.e2set, str(self.setextruder2))
		self.set = True
	def setb(self, num):
		self.setbed = num
		self.parent.changeText(self.parent.bedset, str(self.setbed))
		self.set = True

	def run(self):
		while(True):
			time.sleep(1)
			self.parent.updatetemperatures()
			# if self.set = True:
			# 	self.parent.serial.send_serial('M104' )
			# 	self.set = False