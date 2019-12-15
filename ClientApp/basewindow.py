from PyQt5 import QtCore, QtGui, QtWidgets


class BaseWindow(QtWidgets.QWidget):
	def __init__(self, parent = None):
		super(BaseWindow,self).__init__()
		self.fullscreen = False
		self.parent = parent
		self.notification = None

		if(parent != None):
			if(self.parent.fullscreen):self.fullscreen = True

	def back(self):
		if self.fullscreen:
			self.parent.showFullScreen()
		else:
			self.parent.show()
		self.close()

	def show(self):
		self.move(QtWidgets.qApp.desktop().availableGeometry().center() - self.rect().center())
		super(BaseWindow,self).show()
		
		if(self.parent != None):
			if(self.parent.notification!=None):
				self.notification = self.parent.notification
		if(self.notification != None):
			self.notification.parent = self
			self.notification.show()