from qt.temperaturewindow2 import *
from PyQt5.QtCore import Qt
from temp import *

mats = ['m1', 'm2', 'm3']
periphs = ['e1', 'e2', 'bed', 'all']

class TemperatureWindow(QtWidgets.QWidget, Ui_TemperatureWindow):
	def __init__(self, serial, parent = None):
		super(TemperatureWindow, self).__init__()
		self.setupUi(self)
		
		if parent.fullscreen: self.fullscreen = True
		else: self.fullscreen = False
		if self.fullscreen: 
			self.setWindowState(self.windowState() | Qt.WindowFullScreen)

		self.serial = serial
		self.parent = parent
		self.temphandler = temphandler(serial, self)
		self.temphandler.start()
		self.inittextformat(self.e1temp)
		self.inittextformat(self.e2temp)
		self.inittextformat(self.bedtemp)
		self.inittextformat(self.e1set)
		self.inittextformat(self.e2set)
		self.inittextformat(self.bedset)
		self.changeText(self.e1set, '0')
		self.changeText(self.e2set, '0')
		self.changeText(self.bedset, '0')

		self.initpreheatbuttons()

		self.Back.clicked.connect(self.close)
		self.CoolDown.clicked.connect(self.cool)
		self.fanon = False
		self.fanofficon = QtGui.QIcon()
		self.fanofficon.addPixmap(QtGui.QPixmap("img/fanoff.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.fanonicon = QtGui.QIcon()
		self.fanonicon.addPixmap(QtGui.QPixmap("img/fanon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.Fan.clicked.connect(self.fan)

	def initpreheatbuttons(self):
		for m in mats:
			for p in periphs:
				getattr(self, m+p).clicked.connect(getattr(getattr(self.temphandler, m), p +'set'))

				#getattr(self.temphandler, m+p).clicked.connect()
		# getattr(self.temphandler, attr+'pre')
	def fan(self):
		if self.fanon:
			self.Fan.setIcon(self.fanofficon)
			self.Fan.setIconSize(QtCore.QSize(65, 65))
			self.fanon = False
		elif not self.fanon:
			self.Fan.setIcon(self.fanonicon)
			self.Fan.setIconSize(QtCore.QSize(65, 65))
			self.fanon = True
	def cool(self):
		self.serial.send_serial('M140 S0')
		self.serial.send_serial('M104 T0 S0')
		self.serial.send_serial('M104 T1 S0')
		self.changeText(self.e1set, '0')
		self.changeText(self.e2set, '0')
		self.changeText(self.bedset, '0')

	def updatetemperatures(self):
		self.changeText(self.e1temp, str(int(self.serial.data.temp["T0"][0])))
		self.changeText(self.e2temp, str(int(self.serial.data.temp["T1"][0])))
		self.changeText(self.bedtemp, str(int(self.serial.data.temp["B"][0])))
		# self.changeText(self.e1set, str(self.serial.data.temp["T0"][1]))
		# self.changeText(self.e2set, str(self.serial.data.temp["T1"][1]))
		# self.changeText(self.bedset, str(self.serial.data.temp["B"][1]))

	def changeText(self, label, text):
		tmp = QtWidgets.QApplication.translate("TemperatureWindow",label.format[0]+text+label.format[1],None,-1)
		label.setText(tmp)
	def inittextformat(self,label):
		label.format = label.text()
		label.format = label.format.encode("utf-8").split("-----")