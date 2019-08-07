from qt.temperaturewindow import *
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
		if self.fullscreen: self.showFullScreen()

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

		self.initpreheatbuttons()

		self.Back.clicked.connect(self.close)
		self.CoolDown.clicked.connect(self.cool)

	def initpreheatbuttons(self):
		for m in mats:
			for p in periphs:
				getattr(self, m+p).clicked.connect(getattr(getattr(self.temphandler, m), p +'set'))

				#getattr(self.temphandler, m+p).clicked.connect()
		# getattr(self.temphandler, attr+'pre')
	def cool(self):
		self.serial.send_serial('M104 B0 S0')
		self.serial.send_serial('M104 T0 S0')
		self.serial.send_serial('M104 T1 S0')
		self.changeText(self.e1set, '0')
		self.changeText(self.e2set, '0')
		self.changeText(self.bedset, '0')

	def updatetemperatures(self):
		self.changeText(self.e1temp, str(self.serial.data.temp["T0"][0]))
		self.changeText(self.e2temp, str(self.serial.data.temp["T1"][0]))
		self.changeText(self.bedtemp, str(self.serial.data.temp["B"][0]))

	def changeText(self, label, text):
		tmp = QtWidgets.QApplication.translate("GigabotModule",label.format[0]+text+label.format[1],None,-1)
		label.setText(tmp)
	def inittextformat(self,label):
		label.format = label.text()
		label.format = label.format.encode("utf-8").split("-----")