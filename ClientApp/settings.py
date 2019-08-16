from qt.settingswindow import *
from PyQt5.QtCore import Qt
from serialsetup import *
from server import *


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

		self.Serial.clicked.connect(self.serialpop)
		self.Server.clicked.connect(self.serverpop)
		self.Back.clicked.connect(self.close)


	def serialpop(self):
		if self.fullscreen: self.serial_pop.showFullScreen()
		else: self.serial_pop.show()
	def serverpop(self):
		if self.fullscreen: self.server_pop.showFullScreen()
		else: self.server_pop.show()
	