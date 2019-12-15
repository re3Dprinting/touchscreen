from PyQt5 import QtCore, QtGui, QtWidgets


class BaseWindow(QtWidgets.QWidget):
	def __init__(self, parent = None):
		super(BaseWindow,self).__init__()
		self.fullscreen = False
		self.parent = parent

		if(parent != None):
			if(self.parent.fullscreen):self.fullscreen = True

	def back(self):
		if self.fullscreen:
			self.parent.showFullScreen()
		else:
			self.parent.show()
			self.close()