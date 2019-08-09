from qt.temperaturewindow import *
from notactiveprint_wid import *
from activeprint_wid import *
from PyQt5.QtCore import Qt
from temp import *

mats = ['m1', 'm2', 'm3']
periphs = ['e1', 'e2', 'bed', 'all']

class TemperatureWindow(QtWidgets.QWidget, Ui_TemperatureWindow):
	def __init__(self, serial, parent = None):
		super(TemperatureWindow, self).__init__()
		self.setupUi(self)
		
		# if parent.fullscreen: self.fullscreen = True
		# else: self.fullscreen = False
		# if self.fullscreen: 
		# 	self.setWindowState(self.windowState() | Qt.WindowFullScreen)

		self.serial = serial
		self.parent = parent
		self.temphandler = temphandler(serial, self)
		self.temphandler.start()

		self.ActivePrintWid = ActivePrintWidget(self)
		self.NotActivePrintWid = NotActivePrintWidget(self)
		self.gridLayout.addWidget(self.NotActivePrintWid, 2, 0, 1, 1)
		self.gridLayout.addWidget(self.ActivePrintWid,2,0,1,1)
		self.ActivePrintWid.hide()

		#self.temphandler.updatetemperatures.connect(self.updatetemperatures)
		self.inittextformat(self.e1temp)
		self.inittextformat(self.e2temp)
		self.inittextformat(self.bedtemp)
		self.inittextformat(self.e1set)
		self.inittextformat(self.e2set)
		self.inittextformat(self.bedset)
		self.changeText(self.e1set, '0')
		self.changeText(self.e2set, '0')
		self.changeText(self.bedset, '0')

		self.setbuttonstyle(self.e1img)
		self.setbuttonstyle(self.e2img)
		self.setbuttonstyle(self.bedimg)

		self.initposnegbuttons()

#		Dynamic Icons
		self.fanon = False
		self.fanofficon = QtGui.QIcon()
		self.fanofficon.addPixmap(QtGui.QPixmap("img/fanoff.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.fanonicon = QtGui.QIcon()
		self.fanonicon.addPixmap(QtGui.QPixmap("img/fanon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.ActivePrintWid.Fan.clicked.connect(self.fan)
		self.NotActivePrintWid.Fan.clicked.connect(self.fan)

		self.unheated = QtGui.QIcon()
		self.bedheated1 = QtGui.QIcon()
		self.bedheated2 = QtGui.QIcon()
		self.unheated.addPixmap(QtGui.QPixmap("img/bed_unheated.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.bedheated1.addPixmap(QtGui.QPixmap("img/bed_heated1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.bedheated2.addPixmap(QtGui.QPixmap("img/bed_heated2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)


#		Initilization for Printing and Not-Printing Widgets.
		
		self.ActivePrintWid.Back.clicked.connect(self.close)

		self.initpreheatbuttons()
		self.NotActivePrintWid.Back.clicked.connect(self.close)
		self.NotActivePrintWid.CoolDown.clicked.connect(self.cool)

	def activeprint(self):
		self.NotActivePrintWid.hide()
		self.ActivePrintWid.show()

	def notactiveprint(self):
		self.NotActivePrintWid.show()
		self.ActivePrintWid.hide()

	def initposnegbuttons(self):
		for p in periphs:
			if p == "all": continue
			getattr(self, p+ "pos").clicked.connect(getattr(self.temphandler, "increment_"+p))
			getattr(self, p+ "neg").clicked.connect(getattr(self.temphandler, "decrement_"+p))

	def initpreheatbuttons(self):
		for m in mats:
			for p in periphs:
				getattr(self.NotActivePrintWid, m+p).clicked.connect(getattr(getattr(self.temphandler, m), p +'set'))

	def fan(self):
		if self.serial.is_open:
			if self.fanon:
				self.serial.send_serial('M106 S0')
				self.ActivePrintWid.Fan.setIcon(self.fanofficon)
				self.ActivePrintWid.Fan.setIconSize(QtCore.QSize(65, 65))
				self.NotActivePrintWid.Fan.setIcon(self.fanofficon)
				self.NotActivePrintWid.Fan.setIconSize(QtCore.QSize(65, 65))
				self.fanon = False
			elif not self.fanon:
				self.serial.send_serial('M106 S255')
				self.ActivePrintWid.Fan.setIcon(self.fanonicon)
				self.ActivePrintWid.Fan.setIconSize(QtCore.QSize(65, 65))
				self.NotActivePrintWid.Fan.setIcon(self.fanonicon)
				self.NotActivePrintWid.Fan.setIconSize(QtCore.QSize(65, 65))
				self.fanon = True

	def cool(self):
		self.temphandler.sete1(0)
		self.temphandler.sete2(0)
		self.temphandler.setb(0)
		
	def updatetemperatures(self):
		self.changeText(self.e1temp, str(int(self.serial.data.temp["T0"][0])))
		self.changeText(self.e2temp, str(int(self.serial.data.temp["T1"][0])))
		self.changeText(self.bedtemp, str(int(self.serial.data.temp["B"][0])))

	def changeText(self, label, text):
		if self.serial.is_open: 
			tmp = QtWidgets.QApplication.translate("TemperatureWindow",label.format[0]+text+label.format[1],None,-1)
			label.setText(tmp)
	def inittextformat(self,label):
		label.format = label.text()
		label.format = label.format.encode("utf-8").split("-----")
	def setbuttonstyle(self,obj):
		obj.setStyleSheet("QPushButton{background: rgba(255,255,255,0); outline: none; border: none;}")

