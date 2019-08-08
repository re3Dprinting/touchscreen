from qt.controlwindow import *
from PyQt5.QtCore import Qt
from axis import *

increments_str = ["01", "1","10","100"]
increments_int = ['0.1', '1', '10', '100']

class ControlWindow(QtWidgets.QWidget, Ui_ControlWindow):
	def __init__(self, serial, parent = None):
		super(ControlWindow, self).__init__()
		self.setupUi(self)

		if parent.fullscreen: self.fullscreen = True
		else: self.fullscreen = False
		if self.fullscreen: 
			self.setWindowState(self.windowState() | Qt.WindowFullScreen)
		
		self.parent = parent
		self.setWindowFlags(Qt.Tool)
		self.serial = serial

		self.xinc = None
		self.yinc = None
		self.zinc = None
		self.einc = None
		self.currentextruder = None

		self.parent.setbuttonstyle(self.Back)
		self.parent.setbuttonstyle(self.DisableMotors)
		self.parent.setbuttonstyle(self.HomeAll)
		self.parent.setbuttonstyle(self.HomeXY)
		self.parent.setbuttonstyle(self.HomeZ)
		self.xbutton = self.AddButtontoGroup("x")
		self.ybutton = self.AddButtontoGroup("y")
		self.zbutton = self.AddButtontoGroup("z")
		self.ebutton = self.AddButtontoGroup("e")
		self.extruder = QtWidgets.QButtonGroup(self)

#	Setup for the Extruder button group
		self.SetButtonSettings(self.E1)
		self.SetButtonSettings(self.E2)
		self.extruder.addButton(self.E1)
		self.E1.setChecked(False)
		self.E1.setChecked(True)
		self.extruder.addButton(self.E2)
		self.currentextruder = self.extruder.checkedButton().text()
		self.extruder.buttonClicked.connect(self.updatecurrentextruder)

		self.xaxis = Axis("x", self, 508, 508)
		self.yaxis = Axis("y", self, 463, 0)
		self.zaxis = Axis("z", self, 550, 0)
		self.eaxis = Axis("e", self)
		# self.init_increment()
		self.HomeXY.clicked.connect(self.homexy)
		self.HomeZ.clicked.connect(self.homez)
		self.HomeAll.clicked.connect(self.homeall)
		self.Back.clicked.connect(self.close)
		self.DisableMotors.clicked.connect(self.disablemotors)
		
	def disablemotors(self):
		self.serial.send_serial('M18')

	def homexy(self):
		self.serial.send_serial('G28 XY')
		#self.serial.send_serial('M114')
		# self.xaxis.position = self.xaxis.home
		# self.yaxis.position = self.yaxis.home
	def homez(self):
		self.serial.send_serial('G28 Z')
		#self.serial.send_serial('M114')
		# self.zaxis.position = self.zaxis.home
	def homeall(self):
		self.serial.send_serial('G28')
		# self.serial.send_serial('M114')
		# self.xaxis.position = self.xaxis.home
		# self.yaxis.position = self.yaxis.home
		# self.zaxis.position = self.zaxis.home

	def updatecurrentextruder(self):
		self.currentextruder = self.extruder.checkedButton().text()

	def AddButtontoGroup(self, axis):
		group = QtWidgets.QButtonGroup(self)
		for i in increments_str:
			att = axis + "m" + i
			self.SetButtonSettings(getattr(self,att))
			group.addButton(getattr(self,att))
		#group.clearCheck()
		getattr(self, axis+ "m"+"10").setChecked(False)
		getattr(self, axis+ "m"+"10").setChecked(True)
		return group
	def SetButtonSettings(self,obj):
		obj.setCheckable(True)
		obj.setStyleSheet("QPushButton:checked {background: rgba(255,255,255,1); font: 14pt 'Ubuntu'; border: 2px solid #888} \
			QPushButton{background: rgba(255,255,255,0); font: 14pt 'Ubuntu'; outline: none;}")
