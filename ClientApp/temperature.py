from qt.temperaturewindow import *
from PyQt5.QtCore import Qt


class TemperatureWindow(QtWidgets.QWidget, Ui_TemperatureWindow):
	def __init__(self, parent = None):
		super(TemperatureWindow, self).__init__()
		self.setupUi(self)
		self.showFullScreen()
		self.Back.clicked.connect(self.close)