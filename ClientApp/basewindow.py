from PyQt5 import QtCore, QtGui, QtWidgets


class BaseWindow(QtWidgets.QWidget):
	def __init__(self, parent = None):
		super(BaseWindow,self).__init__()
		self.fullscreen = False
		self.parent = parent
		self.notification = None
		self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint)
		if(parent != None and self.parent.fullscreen):
			self.fullscreen = True
			self.setWindowState(self.windowState() | QtCore.Qt.WindowFullScreen)

	def back(self):
		self.parent.show()
		self.close()

	def show(self):
		self.move(QtWidgets.qApp.desktop().availableGeometry().center() - self.rect().center())
		super(BaseWindow,self).show()
		
		if(self.parent != None):
			if(self.parent.notification != None):
				self.notification = self.parent.notification

		if(self.notification != None):
			self.notification.parent = self
			self.notification.show()
			self.notification.activateWindow()
			# print(self.notification.hasFocus())