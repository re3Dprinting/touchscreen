from qt.controlwindow import *
from PyQt5.QtCore import Qt

increments_str = ["01", "1","10","100"]
increments_int = ['0.1', '1', '10', '100']
axis = ['x', 'y', 'z', 'e']
Axis = ['X', 'Y', 'Z', 'E']

class ControlWindow(QtWidgets.QWidget, Ui_ControlWindow):
	def __init__(self, serial, parent = None):
		super(ControlWindow, self).__init__()
		self.setupUi(self)
		if parent.fullscreen: self.fullscreen = True
		if self.fullscreen: self.showFullScreen()
		self.parent = parent
		self.setWindowFlags(Qt.Tool)
		self.showFullScreen()
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
		self.E1.setChecked(True)
		self.extruder.addButton(self.E2)
		self.currentextruder = self.extruder.checkedButton().text()
		self.extruder.buttonClicked.connect(self.updatecurrentextruder)

		self.init_increment()
		self.Back.clicked.connect(self.close)
		

		#print self.xbutton.buttonClicked.connect(self.checkincrement)


	def init_movement(self):
		for ax in Axis:
			getattr(self, ax + "Pos").buttonClicked.connect()
			getattr(self, ax + "Neg").buttonClicked.connect()

#	for all button groups, initialize the increment values 
#	self.xbutton.checkedButton().text()
#	initializes attributes: self.xinc, self.yinc, self.zinc, self.einc
	def init_increment(self):
		for ax in axis:
			inc = getattr(self,ax +"button").checkedButton().text()
			setattr(self, ax + "inc", inc)
			getattr(self, ax + "button").buttonClicked.connect(getattr(self,"updateincrement"+ax))

	def updateincrementx(self):
		self.xinc = self.xbutton.checkedButton().text()
		print self.xinc
	def updateincrementy(self):
		self.yinc = self.ybutton.checkedButton().text()
	def updateincrementz(self):
		self.zinc = self.zbutton.checkedButton().text()
	def updateincremente(self):
		self.einc = self.ebutton.checkedButton().text()
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
