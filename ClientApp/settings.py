from qt.settingswindow import *
from PyQt5.QtCore import Qt
from serialsetup import *


class SettingsWindow(QtWidgets.QWidget, Ui_SettingsWindow):
	def __init__(self, client_obj, serial_obj, parent = None):
		super(SettingsWindow, self).__init__()
		self.setupUi(self)
		self.client_obj = client_obj
		self.serial_obj = serial_obj
		if parent.fullscreen: self.fullscreen = True
		else: self.fullscreen = False
		# if self.fullscreen: 
		# 	self.setWindowState(self.windowState() | Qt.WindowFullScreen)
		self.parent = parent
		self.parent.setbuttonstyle(self.Serial)
		self.parent.setbuttonstyle(self.Server)

		self.ser_pop = SerialWindow(self.serial_obj, self)
		self.Serial.clicked.connect(self.serialpop)
		self.Back.clicked.connect(self.close)

	def serialpop(self):
		if self.fullscreen: self.ser_pop.showFullScreen()
		else: self.ser_pop.show()
