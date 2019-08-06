from qt.controlwindow import *
from PyQt5.QtCore import Qt

increments = ["01", "1","10","100"]
class ControlWindow(QtWidgets.QWidget, Ui_ControlWindow):
	def __init__(self, parent = None):
		super(ControlWindow, self).__init__()
		self.setupUi(self)
		self.parent = parent
		self.setWindowFlags(Qt.Tool)
		self.showFullScreen()
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
		self.SetButtonSettings(self.E1)
		self.SetButtonSettings(self.E2)
		self.extruder.addButton(self.E1)
		self.extruder.addButton(self.E2)
		self.Back.clicked.connect(self.close)


	def AddButtontoGroup(self, axis):
		group = QtWidgets.QButtonGroup(self)
		for i in increments:
			att = axis + "m" + i
			self.SetButtonSettings(getattr(self,att))
			group.addButton(getattr(self,att))
		#group.clearCheck()
		getattr(self, axis+ "m"+"10").setChecked(False)
		getattr(self, axis+ "m"+"10").setChecked(True)
		return group
	def SetButtonSettings(self,obj):
		obj.setCheckable(True)
		obj.setStyleSheet("QPushButton{font: 14pt 'Ubuntu';} \
			QPushButton:checked {background: rgba(255,255,255,0); font: 14pt 'Ubuntu'; outline: none;}")
